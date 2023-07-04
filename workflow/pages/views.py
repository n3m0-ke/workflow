from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Q, Exists, OuterRef
from django.contrib.auth.decorators import login_required
from users.models import CapacityChoices, Director, Editor, Journalist
from .models import Project, Task, Article, ArticleSection, ProjectStatusChoices, ProposedTitleSubText, TaskStatusChoices, UserNotification, TaskNotification, Instruction, SubmissionStatusChoices, PhotoGallery
from django.utils import timezone
from datetime import time, datetime

#Journalist Views

@login_required
def test_page(request):
    context={}
    return render(request, "testpage.html", context)

@login_required
def login_redirect(request):
    user = request.user
    capacity = user.profile.capacity
    print(capacity)
    print(user.profile.id_card_number)

    if capacity == CapacityChoices.WRITER:
        return redirect('journalist-home')
    elif capacity == CapacityChoices.PHOTOJOURNALIST:
        return redirect('journalist-home')
    elif capacity == CapacityChoices.EDITOR:
        return redirect('editor-home')
    elif capacity == CapacityChoices.DIRECTOR:
        return redirect('director-home')
    else:
        return redirect('logout')


@login_required
def journalist_dashboard_view(request):
    user = request.user
    if((user.profile.capacity!=CapacityChoices.WRITER) and (user.profile.capacity!=CapacityChoices.PHOTOJOURNALIST)):
        messages.error('your are not allowed to access the page.')
        return redirect('logout') 
    context={}
    context['page_title'] = 'Dashboard' 
    return render(request, "journalist/dashboard.html", context)

@login_required
def journalist_article_list_view(request):
    user = request.user
    if((user.profile.capacity!=CapacityChoices.WRITER) and (user.profile.capacity!=CapacityChoices.PHOTOJOURNALIST)):
        messages.error('your are not allowed to access the page.')
        return redirect('logout') 
    context={}
    context['page_title'] = 'Articles List'

    journalist = Journalist.objects.get(user=user)

    incomplete_tasks = journalist.tasks.exclude(progress=100).all()
    complete_tasks = journalist.tasks.filter(progress=100).all()

    context['complete_tasks'] = complete_tasks 
    context['incomplete_tasks'] = incomplete_tasks    
    return render(request, "journalist/article-list.html", context)

@login_required
def journalist_current_article_view(request, task_id):
    user = request.user
    if((user.profile.capacity!=CapacityChoices.WRITER) and (user.profile.capacity!=CapacityChoices.PHOTOJOURNALIST)):
        messages.error('your are not allowed to access the page.')
        return redirect('logout') 
    
    journalist_user = Journalist.objects.get(user=user)
    context={}
    context['page_title'] = 'Article'
    capacity = user.profile.capacity   

    task = Task.objects.get(id=task_id)
    instructions = Instruction.objects.filter(task=task, journalist=journalist_user)
    task_notifications = TaskNotification.objects.filter(task=task)

    
    context['task'] = task
    context['instructions'] = instructions
    context['task_notifications'] = task_notifications

    # If statemtn for usertype to go to current-article-2
    if capacity == CapacityChoices.WRITER:
        # check if Article is created if not create + section
        article = Article.objects.filter(task=task).first()
        if(not(article)):
            article = Article(task=task)
            article.save()

            section = ArticleSection(article=article, journalist=journalist_user)
            section.save()

        # check if section is created if not create
        section = ArticleSection.objects.filter(article=article, journalist=journalist_user).first()
        
        if(not(section)):
            section = ArticleSection(article=article, journalist=journalist_user)
            section.save()
        
        proposed_title_subtext = ProposedTitleSubText.objects.filter(journalist=journalist_user, article=article).first()

        if (request.method=='POST' and ('section-text' in request.POST)):
            section_sub_errors = []
            section_sub_messages = []

            proposed_title_subtext_id = request.POST.get('proposed-title-subtext-id') 
            section_id = request.POST.get('section-id')
            proposed_title = request.POST.get('proposed-title')
            proposed_subtext = request.POST.get('proposed-subtext')
            proposed_section_title = request.POST.get('proposed-section-title')
            section_text = request.POST.get('section-text')
            action = request.POST.get('action')

            # save proposed things
            # save 

            if(proposed_title or proposed_subtext):

                # get proposed details if exists
                if(proposed_title_subtext_id!=''):
                    proposed_title_subtext = ProposedTitleSubText.objects.get(id=proposed_title_subtext_id)

                if(not(proposed_title_subtext)):
                    proposed_title_subtext = ProposedTitleSubText(journalist=journalist_user, article=article)
                
                if(proposed_title_subtext.title != proposed_title):
                    proposed_title_subtext.title = proposed_title
                    proposed_title_subtext.save()
                    
                    task_notification_message = f'{user.first_name} {user.last_name} proposed a title for the Article -> {proposed_title}'
                    current_task_status = task.status
                    task_notification = TaskNotification(creation_time=timezone.now() ,task=task, message=task_notification_message, current_status=current_task_status)
                    task_notification.save()
                
                if(proposed_title_subtext.subtext != proposed_subtext):
                    proposed_title_subtext.subtext = proposed_subtext
                    proposed_title_subtext.save()
                    
                    task_notification_message = f'{user.first_name} {user.last_name} proposed a title for the Article -> {proposed_subtext}'
                    current_task_status = task.status
                    task_notification = TaskNotification(creation_time=timezone.now() ,task=task, message=task_notification_message, current_status=current_task_status)
                    task_notification.save()


                section_sub_messages.append("Proposed Article title and/or subtext saved successfully")

            
            section = ArticleSection.objects.get(id=section_id)
            section.section_title = proposed_section_title
            section.section_text = section_text
            section.save()
            section_sub_messages.append("Article section title and body-text saved successfully")

            task_notification_message = f'{user.first_name} {user.last_name} saved their article section title and body-text'
            current_task_status = task.status
            task_notification = TaskNotification(creation_time=timezone.now() ,task=task, message=task_notification_message, current_status=current_task_status)
            task_notification.save()

            task_notifications = TaskNotification.objects.filter(task=task)
            context['task_notifications'] = task_notifications

            context['section_sub_messages'] = section_sub_messages

            if action == 'submit':
                # get submission status
                section.submission_status = SubmissionStatusChoices.SUBMITTED 
                section.save()               
                
                # update progress
                number_of_sections = article.article_sections.count()
                photo_gallery = PhotoGallery.objects.filter(task=task).first()

                if(photo_gallery):
                    total = number_of_sections + 1
                
                else:
                    total = number_of_sections
                
                #check number of submitted
                number_of_submitted_sections = article.article_sections.filter(submission_status=SubmissionStatusChoices.SUBMITTED).count()

                if(photo_gallery and photo_gallery.submission_status=='submitted'):
                    total_submitted = number_of_submitted_sections + 1
                
                else:
                    total_submitted = number_of_submitted_sections
                
                if(total_submitted>0):
                    progress = int(total_submitted/total)*100
                    task.progress = progress
                    task.save()
                
                if(task.progress==100):
                    task.status = TaskStatusChoices.COMPLETED
                    task.end_date_time = timezone.now()
                    task.save()

                task_notification_message = f'{user.first_name} {user.last_name} submitted their article section title and body-text'
                current_task_status = task.status
                task_notification = TaskNotification(creation_time=timezone.now() ,task=task, message=task_notification_message, current_status=current_task_status)
                task_notification.save()

        context['article'] = article
        context['section'] = section
        print(section.submission_status)
        context['proposed_title_subtext'] = proposed_title_subtext
        return render(request, "journalist/current-article.html", context)
    
    elif capacity == CapacityChoices.PHOTOJOURNALIST:
        return render(request, "journalist/current-article-2.html", context)

@login_required
def journalist_reviews_view(request):
    user = request.user
    if((user.profile.capacity!=CapacityChoices.WRITER) and (user.profile.capacity!=CapacityChoices.PHOTOJOURNALIST)):
        messages.error('your are not allowed to access the page.')
        return redirect('logout') 
    context={}
    context['page_title'] = 'Reviews'
    return render(request, "journalist/reviews.html", context)

@login_required
def journalist_submitted_articles_view(request):
    user = request.user
    if((user.profile.capacity!=CapacityChoices.WRITER) and (user.profile.capacity!=CapacityChoices.PHOTOJOURNALIST)):
        messages.error('your are not allowed to access the page.')
        return redirect('logout') 
    context={}
    context['page_title'] = 'Article Feedback'
    return render(request, "journalist/submitted-articles.html", context)

@login_required
def journalist_messages_view(request):
    user = request.user
    if((user.profile.capacity!=CapacityChoices.WRITER) and (user.profile.capacity!=CapacityChoices.PHOTOJOURNALIST)):
        messages.error('your are not allowed to access the page.')
        return redirect('logout') 
    context={}
    return render(request, "journalist/messages.html", context)

@login_required
def journalist_notifications_view(request):
    user = request.user
    if((user.profile.capacity!=CapacityChoices.WRITER) and (user.profile.capacity!=CapacityChoices.PHOTOJOURNALIST)):
        messages.error('your are not allowed to access the page.')
        return redirect('logout') 
    context={}
    context['page_title'] = 'Notifications'
    return render(request, "journalist/notifications.html", context)

@login_required
def journalist_profile_view(request):
    user = request.user
    if((user.profile.capacity!=CapacityChoices.WRITER) and (user.profile.capacity!=CapacityChoices.PHOTOJOURNALIST)):
        messages.error('your are not allowed to access the page.')
        return redirect('logout') 
    context={}
    context['page_title'] = 'Profile Settings'
    return render(request, "journalist/profile-settings.html", context)


@login_required# Editors Views
def editor_dashboard_view(request):
    user = request.user
    if(user.profile.capacity!=CapacityChoices.EDITOR):
        messages.error('your are not allowed to access the page.')
        return redirect('logout')    
    
    editor_user = Editor.objects.get(user=user)
    context={}
    context['page_title'] = 'Dashboard'
    return render(request, "editor/dashboard.html", context)

@login_required
def editor_article_list_view(request):
    user = request.user
    if(user.profile.capacity!=CapacityChoices.EDITOR):
        messages.error('your are not allowed to access the page.')
        return redirect('logout')    
    
    editor_user = Editor.objects.get(user=user)    
    context={}
    new_task_messages=''
    new_task_errors=[]

    if (request.method=='POST' and ('journalist' in request.POST)):
        task_id = request.POST.get('setupTaskId')
        journalist_ids = []
        instructions_list = []
        for key,value in request.POST.items():
            if "journalist" in key:
                journalist_ids.append(value)
            if "instructions" in key:
                instructions_list.append(value)
        
        task = Task.objects.get(id=task_id)

        for journalist_id in journalist_ids:
            index = journalist_ids.index(journalist_id)

            journalist = Journalist.objects.get(id=journalist_id)
            journalist_user = journalist.user
            task.journalists.add(journalist)

            journalist_instructions = instructions_list[index]
            instruction_object = Instruction(task=task, instruction=journalist_instructions, journalist=journalist)
            instruction_object.save()

            # notify editor and add task notification
            user_notification_message = f'You have been assigned a new Task {task.title} by Editor {request.user.first_name} {request.user.last_name}'
            user_notification = UserNotification(user=journalist_user, message=user_notification_message)
            user_notification.save()

            task_notification_message = f'New Journalist, {journalist_user.first_name} {journalist_user.last_name} added to Task & Assigned Instructions'
            current_task_status = task.status
            task_notification = TaskNotification(creation_time=timezone.now() ,task=task, message=task_notification_message, current_status=current_task_status)
            task_notification.save()
        
        task.status = TaskStatusChoices.IN_PROGRESS
        task.save()
        new_task_messages+='Journalist(s) successfully assigned to task. \n'
        context['new_task_messages'] = new_task_messages

    task_journalists = Journalist.objects.annotate(
        num_incomplete_tasks=Count(
                'tasks',
                filter=Q(tasks__status__in=[TaskStatusChoices.PENDING, TaskStatusChoices.IN_PROGRESS])
            )
        ).annotate(
            has_no_tasks=~Exists(
                Task.objects.filter(journalists=OuterRef('pk'))
            )
        ).filter(
            Q(num_incomplete_tasks__lt=2) | Q(has_no_tasks=True)
        )
    
    

    new_tasks = Task.objects.filter(editor=editor_user, status=TaskStatusChoices.ASSIGNED)
    progressing_tasks = Task.objects.filter(editor=editor_user, status=TaskStatusChoices.IN_PROGRESS)
    complete_tasks = Task.objects.filter(editor=editor_user, status=TaskStatusChoices.COMPLETED)
    context['task_journalists'] = task_journalists
    context['new_tasks'] = new_tasks
    context['progressing_tasks'] = progressing_tasks
    context['complete_tasks'] = complete_tasks
    context['page_title'] = 'Article List'
    return render(request, "editor/article-list.html", context)

@login_required
def editor_current_article_view(request, task_id):
    user = request.user
    if(user.profile.capacity!=CapacityChoices.EDITOR):
        messages.error('your are not allowed to access the page.')
        return redirect('logout')    
    
    editor_user = Editor.objects.get(user=user)
    context={}
    task = Task.objects.get(id=task_id)

    # check for articles, photogallery, article sections and images
    if(hasattr(task, 'article')):
        article = task.article
        context['article'] = article

        proposed_title_subtexts = ProposedTitleSubText.objects.filter(article=article)
        context['proposed_title_subtexts'] = proposed_title_subtexts
    
    if(hasattr(task, 'photo_gallery')):
        photo_gallery = task.photo_gallery
        context['photo_gallery'] = photo_gallery

    print(request.method)

    if(request.method=='POST' and ('approve' in request.POST)):
        proposed_title_subtext_id = request.POST.get('proposed-title-subtext')
        editor_article_title = request.POST.get('article-title')
        editor_article_subtext = request.POST.get('article-subtext')

        proposed_title_subtext = ProposedTitleSubText.objects.get(id=proposed_title_subtext_id)
        proposed_title = proposed_title_subtext.title
        proposed_subtext = proposed_title_subtext.subtext

        if(not(editor_article_title)):
            article_title = proposed_title
        else:
            article_title = editor_article_title
        
        if(not(editor_article_subtext)):
            article_subtext = proposed_subtext
        else:
            article_subtext = editor_article_subtext
        
        article.title = article_title
        article.subtext = article_subtext
        article.save()
        
        task.submission_status = SubmissionStatusChoices.SUBMITTED
        task.save()
        submission_message = "Task approved and submitted for publication"
        
        context['submission_message'] = submission_message

    task_journalists = Journalist.objects.annotate(
        num_incomplete_tasks=Count(
                'tasks',
                filter=Q(tasks__status__in=[TaskStatusChoices.PENDING, TaskStatusChoices.IN_PROGRESS])
            )
        ).annotate(
            has_no_tasks=~Exists(
                Task.objects.filter(journalists=OuterRef('pk'))
            )
        ).filter(
            Q(num_incomplete_tasks__lt=2) | Q(has_no_tasks=True)
        )

    
    task_journalists = task_journalists.exclude(tasks=task)
    task_notifications = TaskNotification.objects.filter(task=task)
    instructions = Instruction.objects.filter(task=task)

    
    
        
    context['task']=task
    context['task_journalists'] = task_journalists
    context['task_notifications'] = task_notifications
    context['instructions'] = instructions
    context['page_title'] = 'Article View'

    # If statemtn for usertype to go to current-article-2
    return render(request, "editor/current-article.html", context)

@login_required
def editor_reviews_view(request):
    user = request.user
    if(user.profile.capacity!=CapacityChoices.EDITOR):
        messages.error('your are not allowed to access the page.')
        return redirect('logout')    
    
    editor_user = Editor.objects.get(user=user)
    context={}
    context['page_title'] = 'Reviews'
    return render(request, "editor/reviews.html", context)

@login_required
def editor_submitted_articles_view(request):
    user = request.user
    if(user.profile.capacity!=CapacityChoices.EDITOR):
        messages.error('your are not allowed to access the page.')
        return redirect('logout')    
    
    editor_user = Editor.objects.get(user=user)
    context={}
    context['page_title'] = 'Article Feedback'
    return render(request, "editor/submitted-articles.html", context)

@login_required
def editor_messages_view(request):
    user = request.user
    if(user.profile.capacity!=CapacityChoices.EDITOR):
        messages.error('your are not allowed to access the page.')
        return redirect('logout')    
    
    editor_user = Editor.objects.get(user=user)
    context={}
    context['page_title'] = 'Messages'
    return render(request, "editor/messages.html", context)

@login_required
def editor_notifications_view(request):
    user = request.user
    if(user.profile.capacity!=CapacityChoices.EDITOR):
        messages.error('your are not allowed to access the page.')
        return redirect('logout')    
    
    editor_user = Editor.objects.get(user=user)
    context={}
    context['page_title'] = 'Notifications'
    return render(request, "editor/notifications.html", context)

@login_required
def editor_profile_view(request):
    user = request.user
    if(user.profile.capacity!=CapacityChoices.EDITOR):
        messages.error('your are not allowed to access the page.')
        return redirect('logout')    
    
    editor_user = Editor.objects.get(user=user)
    context={}
    context['page_title'] = 'Profile Settings'
    return render(request, "editor/profile-settings.html", context)



@login_required# Director's Views
def director_dashboard_view(request):
    user = request.user
    if(user.profile.capacity!=CapacityChoices.DIRECTOR):
        messages.error('your are not allowed to access the page.')
        return redirect('logout')
    

    context={}
    context['page_title'] = 'Dashboard'
    return render(request, "director/dashboard.html", context)

@login_required
def director_article_list_view(request):
    user = request.user
    director_user = Director.objects.get(user=user)
    if(user.profile.capacity!=CapacityChoices.DIRECTOR):
        messages.error('your are not allowed to access the page.')
        return redirect('logout')

    
    context={}
    project_errors = []
    task_errors = []
    task_messages = []
    project_table_errors = []
    project_messages = []

    if (request.method=='POST' and ('project-title' in request.POST)):
        # get post details
        project_title = request.POST.get('project-title')
        project_description = request.POST.get('project-description')
        
        # check if there is a project with same title
        project = Project.objects.filter(title=project_title).first()

        if(project):
            project_errors.append(f'There is a project with title {project_title}. Choose a different title')         
            context['project_errors'] = project_errors

        else:
            new_project = Project(title=project_title, director=director_user, description=project_description, date_of_creation=timezone.now())
            new_project.save()
            project_messages.append(f'{project_title} Project created successfully')
            context['project_messages'] = project_messages
    
    if (request.method=='POST' and ('task-title' in request.POST)):
        # get post details
        task_title = request.POST.get('task-title')
        task_project_id = request.POST.get('task-project-id')
        
        # check if there is a task with same title under same project
        task = Task.objects.filter(title=task_title, project__id=task_project_id).first()

        if(task):   
            task_errors.append(f'There is a task with title {task_title} under the same project. Choose a different title')         
            context['task_errors'] = task_errors

        else:
            task_description = request.POST.get('task-description')         
            task_editor_id = request.POST.get('task-editor-id')
            editor = Editor.objects.get(id=task_editor_id)
            project = Project.objects.get(id=task_project_id)

            deadline_date = request.POST.get('task-enddate')
            deadline_time = request.POST.get('task-endtime')

            # Convert the date and time strings to datetime objects
            date_obj = datetime.strptime(deadline_date, '%Y-%m-%d').date()
            time_obj = datetime.strptime(deadline_time, '%H:%M').time()

            datetime_obj = datetime.combine(date_obj, time_obj)

            new_task = Task(
                title=task_title, 
                editor=editor, 
                description=task_description, 
                start_date=timezone.now().date(), 
                deadline=datetime_obj, 
                project=project, 
                status=TaskStatusChoices.ASSIGNED)
            new_task.save()

            # notify editor and add task notification
            editor_user = editor.user
            user_notification_message = f'You have been assigned a new Task {task_title} by Director {request.user.first_name} {request.user.last_name}'
            user_notification = UserNotification(user=editor_user, message=user_notification_message)
            user_notification.save()

            task_notification_message = f'Task Created & Assigned to Editor {editor_user.first_name} {editor_user.last_name}'
            current_task_status = new_task.status
            task_notification = TaskNotification(creation_time=timezone.now() ,task=new_task, message=task_notification_message, current_status=current_task_status)
            task_notification.save()

            
            task_messages.append(f'{task_title} Task created successfully')
            context['task_messages'] = task_messages
    
    if (request.method=='POST' and ('toggleStatusSub' in request.POST)):
        project_id = request.POST.get('projectid')
        print(project_id)

        # check if project has incomplete tasks
        if(Task.objects.filter(project_id=project_id).exclude(status='completed').exists()):
            project_table_errors.append("There are tasks under this project. Cannot deactivate the project")
            context['project_table_errors'] = project_table_errors
        
        else:
            project = get_object_or_404(Project, id=project_id)
            print("status: ", project.status)
            print("Active status: ", ProjectStatusChoices.ACTIVE)
            print("Inactive status: ", ProjectStatusChoices.DEACTIVATED)
            if(project.status == ProjectStatusChoices.ACTIVE):
                project.status = ProjectStatusChoices.DEACTIVATED
            else:
                project.status = ProjectStatusChoices.ACTIVE
            
            project.save()
            project_messages.append("Project Status updated successfully")
            context['project_messages'] = project_messages
    
    
    if (request.method=='POST' and ('task-id' in request.POST)):
        task = Task.objects.get(id=request.POST.get('task-id'))
        task.status=TaskStatusChoices.APPROVED
        task.save()
        approval_messages = []
        approval_messages.append('Task approved successfully')
        context['approval_messages'] = approval_messages

    projects = Project.objects.filter(director=director_user)
    projects_count = projects.count()

    task_editors = Editor.objects.annotate(
        num_incomplete_tasks=Count(
                'task',
                filter=Q(task__status__in=[TaskStatusChoices.PENDING,TaskStatusChoices.ASSIGNED, TaskStatusChoices.IN_PROGRESS])
            )
        ).annotate(
            has_no_tasks=~Exists(
                Task.objects.filter(editor=OuterRef('pk'))
            )
        ).filter(
            Q(num_incomplete_tasks__lt=3) | Q(has_no_tasks=True)
        )


    context['task_editors'] = task_editors

    tasks = Task.objects.filter(project__in=projects)

    pending_tasks = tasks.exclude(submission_status=SubmissionStatusChoices.SUBMITTED)
    submitted_tasks = tasks.filter(submission_status=SubmissionStatusChoices.SUBMITTED)


    tasks_count = tasks.count()

    context['page_title'] = 'Projects/Tasks List'
    
    context['projects'] = projects
    context['projects_count'] = projects_count

    context['tasks'] = tasks
    context['tasks_count'] = tasks_count

    context['pending_tasks'] = pending_tasks
    context['submitted_tasks'] = submitted_tasks
    
    return render(request, "director/article-list.html", context)

@login_required
def director_current_article_view(request):
    user = request.user
    if(user.profile.capacity!=CapacityChoices.DIRECTOR):
        messages.error('your are not allowed to access the page.')
        return redirect('logout')

    context={}
    context['page_title'] = 'Task View'
    # If statemtn for usertype to go to current-article-2
    return render(request, "director/current-article.html", context)

@login_required
def director_reviews_view(request):
    user = request.user
    if(user.profile.capacity!=CapacityChoices.DIRECTOR):
        messages.error('your are not allowed to access the page.')
        return redirect('logout')

    context={}
    context['page_title'] = 'Reviews Statistics'
    return render(request, "director/reviews.html", context)

@login_required
def director_submitted_articles_view(request):
    user = request.user
    if(user.profile.capacity!=CapacityChoices.DIRECTOR):
        messages.error('your are not allowed to access the page.')
        return redirect('logout')

    context={}
    context['page_title'] = 'Task Feedback'
    return render(request, "director/submitted-articles.html", context)

@login_required
def director_messages_view(request):
    user = request.user
    if(user.profile.capacity!=CapacityChoices.DIRECTOR):
        messages.error('your are not allowed to access the page.')
        return redirect('logout')

    context={}
    context['page_title'] = 'Messages'
    return render(request, "director/messages.html", context)

@login_required
def director_notifications_view(request):
    user = request.user
    if(user.profile.capacity!=CapacityChoices.DIRECTOR):
        messages.error('your are not allowed to access the page.')
        return redirect('logout')

    context={}
    context['page_title'] = 'Notifications'
    return render(request, "director/notifications.html", context)

@login_required
def director_profile_view(request):
    user = request.user
    if(user.profile.capacity!=CapacityChoices.DIRECTOR):
        messages.error('your are not allowed to access the page.')
        return redirect('logout')

    context={}
    context['page_title'] = 'Profile Settings'
    return render(request, "director/profile-settings.html", context)




# Error pages
def handler400(request, exception):
    return render(request, 'error-pages/page-error-400.html', status=400)

def handler403(request, exception):
    return render(request, 'error-pages/page-error-403.html', status=403)

def handler404(request, exception):
    return render(request, 'error-pages/page-error-404.html', status=404)

def handler500(request):
    return render(request, 'error-pages/page-error-500.html', status=500)

def handler503(request):
    return render(request, 'error-pages/page-error-503.html', status=503)
