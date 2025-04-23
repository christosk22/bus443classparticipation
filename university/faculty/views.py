from django.shortcuts import render
from django.http import HttpResponse
from faculty.models import Facultydetails, Awarddetails, Nominationdetails
from django.db import connection
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from openai import OpenAI

# Create your views here.

def chatBot(request):
    client = OpenAI(
        api_key=os.environ.get("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"),
    )

    response = client.responses.create(
        model="gpt-3.5-turbo",
        instructions="You are a helpful assistant.",
        input="How do I check if a Python object is an instance of a class?",
    )

    return HttpResponse(response.output_text)


   



def dashboard(request):
    # select count(*) from faculty_nominationdetails where awardtype = 'Teaching';
    teaching_nominations = Nominationdetails.objects.filter(awardtype="Teaching").count()
    research_nominations = Nominationdetails.objects.filter(awardtype="Research").count()
    outreach_nominations = Nominationdetails.objects.filter(awardtype="Outreach").count()
    
    context = {
        "teaching": teaching_nominations,
        "research": research_nominations,
        "outreach": outreach_nominations
    }
    return render(request, "faculty/dashboard.html", context)


def nominationinfo(request):
    facultydata = Facultydetails.objects.all()
    awarddata = Awarddetails.objects.all()
    nominationdata = Nominationdetails.objects.all()
    context = {'faculty': facultydata, 'award': awarddata, 'nomination': nominationdata}
    return render(request, "faculty/nomination.html", context)

def saveinfo(request):
    if "facultydata" in request.GET and "awarddata" in request.GET:
        # Extract the facultydata from the request object
        faculty = request.GET.get("facultydata")
        award = request.GET.get("awarddata")

        # Django query set statement to get the count of rows where the faculty name exists
        # select count(*) from faculty_nominationdetails where facultyname = 'faculty name'
        facultycount = Nominationdetails.objects.filter(facultyname=faculty).count()

        if facultycount == 0:
            data = Nominationdetails(facultyname=faculty, awardtype=award)
            # insert a new row of data into the Nominationdetails table
            data.save()
            return HttpResponse("success")

    return HttpResponse("error")

@login_required
def home(request):
    #return HttpResponse("This is the home page")
    facultydict = {"facultyname": "Genna Wood"}
    return render (request, "faculty/home.html", facultydict)

def dictfetchall(cursor):
    """
    Return all rows from a cursor as a dict.
    Assume the column names are unique.
    """
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

@login_required
def facultyinfo(request):
    # Django query set statement to retrieve all data from the facultydetails table
    # Django query set is django's abstraction of SQL commands
    data = Facultydetails.objects.all()  # select * from faculty_facultydetails
    #print(data[0]._dict_)
    #cursor = connection.cursor()
    #cursor.execute("SELECT * FROM faculty_facultydetails")
    #data = dictfetchall(cursor) 
    #print(data)
    
    data = Facultydetails.objects.all()  # select * from faculty_facultydetails
    # Creating a paginator object from the Paginator class
    paginator = Paginator(data, 2)

    page = request.GET.get('page')
    page_data = paginator.get_page(page)

    context = {"facultydata": page_data}
    return render(request, "faculty/facultyinfo.html", context)
