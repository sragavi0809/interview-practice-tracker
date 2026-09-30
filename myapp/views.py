
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import date, timedelta

from .models import Question, PracticeResult


# =========================
# 🏠 DASHBOARD
# =========================

@login_required
def home(request):

    # =========================
    # BASIC QUESTION STATISTICS
    # =========================

    total_questions = Question.objects.count()

    practiced_questions = Question.objects.filter(
        practiced=True
    ).count()

    not_practiced_questions = Question.objects.filter(
        practiced=False
    ).count()

    total_categories = Question.objects.values(
        "category"
    ).distinct().count()


    # =========================
    # OVERALL PROGRESS
    # =========================

    if total_questions > 0:

        progress_percentage = (
            practiced_questions / total_questions
        ) * 100

    else:

        progress_percentage = 0


    # =========================
    # DAILY STREAK
    # =========================

    results = PracticeResult.objects.order_by(
        "-practiced_at"
    )

    practiced_dates = set()


    for result in results:

        practiced_dates.add(
            result.practiced_at.date()
        )


    streak = 0


    if practiced_dates:

        today = date.today()

        current_date = today


        while current_date in practiced_dates:

            streak += 1

            current_date -= timedelta(days=1)


    # =========================
    # CATEGORY PROGRESS
    # =========================

    category_progress = []

    categories = Question.objects.values(
        "category"
    ).distinct()


    for category in categories:

        category_name = category["category"]


        total_in_category = Question.objects.filter(
            category=category_name
        ).count()


        practiced_in_category = Question.objects.filter(
            category=category_name,
            practiced=True
        ).count()


        if total_in_category > 0:

            category_percentage = (
                practiced_in_category /
                total_in_category
            ) * 100

        else:

            category_percentage = 0


        category_progress.append(
            {
                "name": category_name,
                "total": total_in_category,
                "practiced": practiced_in_category,
                "percentage": category_percentage
            }
        )


    # =========================
    # ⭐ AVERAGE SCORE
    # =========================

    total_results = PracticeResult.objects.count()


    if total_results > 0:

        total_percentage = sum(
            result.percentage
            for result in PracticeResult.objects.all()
        )

        average_score = (
            total_percentage / total_results
        )

    else:

        average_score = 0


    # =========================
    # 📈 WEEKLY PROGRESS
    # =========================

    today = date.today()

    week_start = today - timedelta(
        days=today.weekday()
    )


    weekly_progress = []


    for i in range(7):

        current_day = week_start + timedelta(
            days=i
        )


        day_results = PracticeResult.objects.filter(
            practiced_at__date=current_day
        )


        practice_count = day_results.count()


        weekly_progress.append(
            {
                "day": current_day.strftime("%a"),
                "date": current_day,
                "count": practice_count
            }
        )


    # =========================
    # 📝 RECENT PRACTICE SESSIONS
    # =========================

    recent_sessions = PracticeResult.objects.order_by(
        "-practiced_at"
    )[:5]


    # =========================
    # SEND DATA TO DASHBOARD
    # =========================

    return render(
        request,
        "myapp/home.html",
        {
            "total_questions": total_questions,
            "practiced_questions": practiced_questions,
            "not_practiced_questions": not_practiced_questions,
            "total_categories": total_categories,
            "progress_percentage": progress_percentage,
            "streak": streak,
            "category_progress": category_progress,

            "average_score": average_score,
            "weekly_progress": weekly_progress,
            "recent_sessions": recent_sessions
        }
    )


# =========================
# 🔐 LOGIN
# =========================

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")


        user = authenticate(
            request,
            username=username,
            password=password
        )


        if user is not None:

            login(request, user)

            return redirect("home")


        else:

            return render(
                request,
                "myapp/login.html",
                {
                    "error": "Invalid username or password."
                }
            )


    return render(
        request,
        "myapp/login.html"
    )


# =========================
# 🚪 LOGOUT
# =========================

def logout_view(request):

    logout(request)

    return redirect("login")


# =========================
# ➕ ADD QUESTION
# =========================

@login_required
def add_question(request):

    if request.method == "POST":

        question = request.POST.get("question")
        category = request.POST.get("category")
        answer = request.POST.get("answer")


        Question.objects.create(
            question=question,
            category=category,
            answer=answer
        )


        return redirect("question_list")


    return render(
        request,
        "myapp/add_question.html"
    )


# =========================
# 📚 QUESTION LIST
# =========================

@login_required
def question_list(request):

    search = request.GET.get("search")
    category = request.GET.get("category")
    status = request.GET.get("status")


    questions = Question.objects.all()


    # Search by question or category

    if search:

        questions = questions.filter(
            Q(question__icontains=search) |
            Q(category__icontains=search)
        )


    # Filter by category

    if category:

        questions = questions.filter(
            category__iexact=category
        )


    # Filter by practice status

    if status == "practiced":

        questions = questions.filter(
            practiced=True
        )


    elif status == "not_practiced":

        questions = questions.filter(
            practiced=False
        )


    # Get unique categories

    categories = Question.objects.values_list(
        "category",
        flat=True
    ).distinct()


    return render(
        request,
        "myapp/question_list.html",
        {
            "questions": questions,
            "search": search,
            "selected_category": category,
            "selected_status": status,
            "categories": categories
        }
    )


# =========================
# ✅ MARK PRACTICED
# =========================

@login_required
def mark_practiced(request, id):

    question = get_object_or_404(
        Question,
        id=id
    )


    question.practiced = True

    question.save()


    return redirect("question_list")


# =========================
# 🗑️ DELETE QUESTION
# =========================

@login_required
def delete_question(request, id):

    question = get_object_or_404(
        Question,
        id=id
    )


    question.delete()


    return redirect("question_list")


# =========================
# ✏️ EDIT QUESTION
# =========================

@login_required
def edit_question(request, id):

    question = get_object_or_404(
        Question,
        id=id
    )


    if request.method == "POST":

        question.question = request.POST.get(
            "question"
        )

        question.category = request.POST.get(
            "category"
        )

        question.answer = request.POST.get(
            "answer"
        )


        question.save()


        return redirect("question_list")


    return render(
        request,
        "myapp/edit_question.html",
        {
            "question": question
        }
    )


# =========================
# 🎯 PRACTICE MODE
# =========================

@login_required
def practice(request):

    questions = Question.objects.all()


    return render(
        request,
        "myapp/practice.html",
        {
            "questions": questions
        }
    )


# =========================
# 💾 SAVE PRACTICE RESULT
# =========================

@login_required
def save_practice_result(request):

    if request.method == "POST":

        total_questions = int(
            request.POST.get(
                "total_questions",
                0
            )
        )


        correct_answers = int(
            request.POST.get(
                "correct_answers",
                0
            )
        )


        score = int(
            request.POST.get(
                "score",
                0
            )
        )


        percentage = float(
            request.POST.get(
                "percentage",
                0
            )
        )


        PracticeResult.objects.create(
            total_questions=total_questions,
            correct_answers=correct_answers,
            score=score,
            percentage=percentage
        )


        return redirect("practice")


    return redirect("practice")




@login_required
def practice_history(request):

    results = PracticeResult.objects.all().order_by(
        "-practiced_at"
    )


    return render(
        request,
        "myapp/practice_history.html",
        {
            "results": results
        }
    )

