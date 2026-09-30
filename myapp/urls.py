
from django.urls import path
from . import views


urlpatterns = [

    # Login / Logout
    path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),


    # Dashboard
    path(
        "",
        views.home,
        name="home"
    ),


    # Questions
    path(
        "questions/",
        views.question_list,
        name="question_list"
    ),

    path(
        "add-question/",
        views.add_question,
        name="add_question"
    ),

    path(
        "edit-question/<int:id>/",
        views.edit_question,
        name="edit_question"
    ),

    path(
        "delete-question/<int:id>/",
        views.delete_question,
        name="delete_question"
    ),

    path(
        "mark-practiced/<int:id>/",
        views.mark_practiced,
        name="mark_practiced"
    ),


    # 🎯 Practice Mode
    path(
        "practice/",
        views.practice,
        name="practice"
    ),


    # 💾 Save Practice Result
    path(
        "save-practice-result/",
        views.save_practice_result,
        name="save_practice_result"
    ),


    # 📅 Practice History
    path(
        "practice-history/",
        views.practice_history,
        name="practice_history"
    ),

]

