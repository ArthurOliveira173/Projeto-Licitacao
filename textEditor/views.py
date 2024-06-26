from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, FileResponse, Http404, HttpResponse
from .models import Document
from .forms import DocumentForm
from licitacaoProj import settings
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
import mimetypes
import os
import io

FILE_PATH = os.path.join(settings.BASE_DIR, r'static\media')

def upload(request):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list')
    else:
        form = DocumentForm()
    return render(request, 'upload.html', {'form': form})


def edit(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if request.method == "POST":
        form = DocumentForm(request.POST, instance=document)
        if form.is_valid():
            form.save()
            return redirect('list')
    else:
        form = DocumentForm(instance=document)
    return render(request, 'edit.html', {'form': form, 'document': document})

def delete(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    document.delete()

    documents = Document.objects.all()
    return redirect('list')

def detail(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    return render(request, 'detail.html', {'document': document})

def list(request):
    documents = Document.objects.all()
    return render(request, 'list.html', {'documents': documents})

# def download(request, document_id):
#     document = get_object_or_404(Document, id=document_id)
#     BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     filename = str(document.title)
#     filepath = BASE_DIR + '\\static\\media\\' + filename
#     path = open(filepath, 'rb')
#     mime_type, _ = mimetypes.guess_type(filepath)
#     response = HttpResponse(path, content_type=mime_type)
#     response['Content-Disposition'] = "attachment; filename=%s" % filename
#     return response

def download(request, document_id):
    #Buffer
    buffer = io.BytesIO()
    #Canvas
    canv = canvas.Canvas(buffer, pagesize=letter, bottomup=0)
    #Text Object
    textOb = canv.beginText()
    textOb.setTextOrigin(inch, inch)
    textOb.setFont("Helvetica", 12)

    #Collect document content
    document = get_object_or_404(Document, id=document_id)
    textOb.textLine(document.content)

    canv.drawText(textOb)
    canv.showPage()
    canv.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename=str(document.title) + ".pdf")

def textEditor(request):
    content = ''
    return render(request, 'textEditor.html', {'content': content})

#PDF CANVAS
# def view_pdf(request):
#     return render(request, 'view_pdf.html')

#PDF & WORD
# def read_pdf(file_path):
#     doc = fitz.open(file_path)
#     content = ''
#     for page in doc:
#         content += page.get_text()
#     return content
#
# def write_pdf(file_path, content):
#     doc = fitz.open()
#     page = doc.new_page()
#     page.insert_text((72, 72), content)  # Position (72, 72) is 1 inch from top-left
#     doc.save(file_path)
#
# def read_docx(file_path):
#     doc = Document(file_path)
#     content = '\n'.join([para.text for para in doc.paragraphs])
#     return content
#
# def write_docx(file_path, content):
#     doc = Document()
#     for line in content.split('\n'):
#         doc.add_paragraph(line)
#     doc.save(file_path)
#
# def index(request):
#     content = ''
#     if os.path.exists(FILE_PATH):
#         content = read_pdf(FILE_PATH)
#     return render(request, 'textEditor.html', {'content': content})
#
# def save(request):
#     if request.method == 'POST':
#         data = request.POST.get('content', '')
#         write_pdf(FILE_PATH, data)
#         return JsonResponse({"status": "success"})
#     return JsonResponse({"status": "failed"})
