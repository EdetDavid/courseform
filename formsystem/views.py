
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from .forms import (
    UserRegistrationForm,
    StudentRegistrationForm,
    HODRegistrationForm,
    CourseFormSubmission,
)
from .models import CourseForm, Department, HOD, Student, SignedCourseForm
from django.shortcuts import get_object_or_404
from django.utils import timezone

from django.http import FileResponse
import io
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from django.templatetags.static import static
import os
from django.conf import settings


def home(request):
    if request.method == "POST":
        if "student_login" in request.POST:
            student_form = AuthenticationForm(request, data=request.POST)
            if student_form.is_valid():
                username = student_form.cleaned_data.get("username")
                password = student_form.cleaned_data.get("password")
                user = authenticate(username=username, password=password)
                if user is not None and hasattr(user, "student"):
                    login(request, user)
                    return redirect("student_dashboard")
        elif "hod_login" in request.POST:
            hod_form = AuthenticationForm(request, data=request.POST)
            if hod_form.is_valid():
                username = hod_form.cleaned_data.get("username")
                password = hod_form.cleaned_data.get("password")
                user = authenticate(username=username, password=password)
                if user is not None and hasattr(user, "hod"):
                    login(request, user)
                    return redirect("hod_dashboard")
    else:
        student_form = AuthenticationForm()
        hod_form = AuthenticationForm()

    return render(
        request,
        "formsystem/home.html",
        {"student_form": student_form, "hod_form": hod_form},
    )


@login_required(login_url="home")
def student_dashboard(request):
    return render(request, "formsystem/student_dashboard.html")


@login_required(login_url="home")
def hod_dashboard(request):
    
    return render(request, "formsystem/hod_dashboard.html")


@login_required(login_url="home")
def profile(request):
    user = request.user
    if hasattr(user, "student"):
        profile = user.student
    elif hasattr(user, "hod"):
        profile = user.hod
    else:
        profile = None

    return render(request, "formsystem/profile.html", {"profile": profile})


@login_required(login_url="home")
def update_profile(request):
    user = request.user
    if hasattr(user, "student"):
        profile = user.student
        form_class = StudentRegistrationForm
    elif hasattr(user, "hod"):
        profile = user.hod
        form_class = HODRegistrationForm
    else:
        profile = None

    if request.method == "POST":
        form = form_class(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = form_class(instance=profile)

    return render(request, "formsystem/update_profile.html", {"form": form})


def about(request):
    return render(request, "formsystem/about.html")


def blog(request):
    return render(request, "formsystem/blog.html")


def register_student(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        student_form = StudentRegistrationForm(request.POST)
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data["password"])
            user.save()
            student = student_form.save(commit=False)
            student.user = user
            student.save()
            login(request, user)
            return redirect("student_dashboard")
    else:
        user_form = UserRegistrationForm()
        student_form = StudentRegistrationForm()
    return render(
        request,
        "formsystem/register_student.html",
        {"user_form": user_form, "student_form": student_form},
    )


def register_hod(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        hod_form = HODRegistrationForm(request.POST)
        if user_form.is_valid() and hod_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data["password"])
            user.save()
            hod = hod_form.save(commit=False)
            hod.user = user
            hod.save()
            login(request, user)
            return redirect("hod_dashboard")
    else:
        user_form = UserRegistrationForm()
        hod_form = HODRegistrationForm()
    return render(
        request,
        "formsystem/register_hod.html",
        {"user_form": user_form, "hod_form": hod_form},
    )


# course forms views


@login_required(login_url="home")
def submit_course_form(request):
    if request.method == "POST":
        form = CourseFormSubmission(request.POST, request.FILES)  
        if form.is_valid():
            course_form = form.save(commit=False)
            student = request.user.student
            course_form.student = student

            # Find the HOD for the student's department
            hod = HOD.objects.get(department=student.department)
            course_form.hod = hod
            
            course_form.save()
            return redirect("student_dashboard")
    else:
        form = CourseFormSubmission()
    return render(request, "formsystem/submit_course_form.html", {"form": form})


@login_required(login_url="home")
def course_forms(request):
    if hasattr(request.user, "hod"):
        department = request.user.hod.department
        # Filter course forms by the department of the students who submitted them
        course_forms = CourseForm.objects.filter(student__department=department)
        return render(
            request,
            "formsystem/course_forms.html",
            {"course_forms": course_forms, "department": department},
        )
    else:
        return redirect("hod_dashboard")




@login_required(login_url="home")
def toggle_is_signed(request, pk):
    course_form = get_object_or_404(CourseForm, pk=pk)
    
    if request.user.hod == course_form.hod:
        # Update the form to mark it as signed
        course_form.is_signed = not course_form.is_signed
        
        if course_form.is_signed:
            # Set the signed_at field to the current date and time when signing the form
            course_form.signed_at = timezone.now()
        else:
            # Optionally, clear the signed_at field if un-signing
            course_form.signed_at = None
        
        course_form.save()
    
    return redirect("course_forms")



@login_required(login_url="home")
def view_course_form(request, pk):
    course_form = get_object_or_404(CourseForm, pk=pk)
    if request.user.hod == course_form.hod:
        # Read the original PDF
        pdf_reader = PdfReader(course_form.form_content.path)
        pdf_writer = PdfWriter()

        # Create a new PDF with the signature
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)

        # Draw the signature image on the new PDF
        signature_path = os.path.join(settings.BASE_DIR, 'static/images/signature.png')
        can.drawImage(signature_path, x=310, y=175, width=1*inch, height=1*inch)  # Customize position and size
        can.showPage()
        can.save()

        # Move to the beginning of the StringIO buffer
        packet.seek(0)
        new_pdf = PdfReader(packet)

        # Merge the new PDF with the existing PDF
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            if page_num == len(pdf_reader.pages) - 1:  # Add signature to the last page
                page.merge_page(new_pdf.pages[0])
            pdf_writer.add_page(page)

        # Save the modified PDF to a buffer
        output = io.BytesIO()
        pdf_writer.write(output)
        output.seek(0)

        # Serve the new PDF
        return FileResponse(output, as_attachment=False, filename="viewed_course_form.pdf")
    else:
        return redirect("home")





@login_required(login_url="home")
def download_course_form(request, pk):
    try:
        # Get the CourseForm by primary key
        course_form = CourseForm.objects.get(pk=pk)

        # Determine the file path to download
        if course_form.is_signed and hasattr(course_form, 'signedcourseform'):
            file_path = course_form.signedcourseform.signed_form.path
        else:
            file_path = course_form.form_content.path

        # Ensure the file exists
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/pdf")
                response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
                return response
        else:
            raise Http404("File does not exist.")

    except CourseForm.DoesNotExist:
        raise Http404("Course form does not exist.")

    except Exception as e:
        return HttpResponse(f"An unexpected error occurred: {str(e)}", status=500)







# @login_required(login_url="home")
# def send_signed_form(request, pk):
#     form = get_object_or_404(CourseForm, pk=pk)

#     if request.method == 'POST':
#         # Update the form to mark it as signed
#         form.is_signed = True
#         form.signed_at = timezone.now()  # Get the current time
#         form.signed_form = request.FILES['signed_form']  # Handle file upload
#         form.save()

#         # Redirect to the course forms page or any other page
#         return redirect('course_forms')

#     return render(request, 'formsystem/send_signed_form.html', {'form': form})




@login_required(login_url="home")
def send_signed_form(request, ):
    course_form = get_object_or_404(CourseForm)

    if request.method == 'POST':
        # # Create a new SignedCourseForm instance
        signed_form = SignedCourseForm()
        signed_form.course_form = course_form
        signed_form.hod = request.user.hod  # Associate with the HOD who signed the form
        signed_form.signed_at = timezone.now()  # Set the current time

        # Save the uploaded file to the SignedCourseForm instance
        if 'signed_form' in request.FILES:
            signed_form.signed_form = request.FILES['signed_form']

        signed_form.save()

        # Update the CourseForm to mark it as signed
        course_form.is_signed = True
        course_form.signed_at = signed_form.signed_at
        course_form.save()

        # Redirect to the course forms page or any other page
        return redirect('course_forms')

    return render(request, 'formsystem/send_signed_form.html', {})


@login_required(login_url="home")
def signed_course_forms(request):
    student = get_object_or_404(Student, user=request.user)
    signed_forms = SignedCourseForm.objects.all()
    return render(request, 'formsystem/signed_course_forms.html', {'signed_forms': signed_forms})


def logout_user(request):
    logout(request)
    return redirect("home")

