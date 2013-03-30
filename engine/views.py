from django.http import HttpResponse
from django.shortcuts import render_to_response
from engine.models import list_object
from engine.models import object_object
from engine.models import parameter_object


from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from engine.models import Document
from engine.forms import DocumentForm


import database_manager
import algorithm_manager
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django import forms

from django.utils import simplejson
from engine.forms import DocumentForm
import datetime
import scipy
import sklearn
import os


###########################################
#   Debugging use
#
###########################################

def list(request):

    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('engine.views.list'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form

    return render_to_response(
        'engine/list.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )




def display_cluster_engine(request):

    algorithms, datasets = database_manager.retrieve_interface_data()
    upload_file_name = ""

	# Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():

            # remove whatever is in there
            now = datetime.datetime.now()
            if now.month < 10:
                mth = str(0)+str(now.month)
            else:
                mth = str(now.month)

            if now.day < 10:
                day = str(0)+str(now.day)
            else:
                day = str(now.day)

            path = '/static_media_clustapp/documents/'+str(now.year)+'/'+mth+'/'+day+'/'
            full_path = os.path.realpath('.')
            os.system('rm '+full_path+path+'*')


            # store uploaded file
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

            upload_file_name = request.FILES['docfile']

            # debugging use, output the newest file uploaded
            print 'Newest File Uploaded'
            os.system('ls '+full_path+path)



            # Redirect to the document list after POST
            #return HttpResponseRedirect(reverse('engine.views.display_cluster_engine'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'engine/engine_interface.html',
        {
            'documents': documents,
            'form': form,
            'algorithms':algorithms,
            'datasets': datasets,
            'upload':upload_file_name,

        },
        context_instance=RequestContext(request)
    )

    """
    algorithms, datasets = database_manager.retrieve_interface_data()

    return render_to_response(
            'engine/engine_interface.html',
            {
                'algorithms':algorithms,
                'datasets': datasets,
            }
    )
    """


def get_parameter_given_algorithm_or_dataset_name(request):
    name = request.GET['algo']
    param_dict = {}
    parameters = database_manager.retrieve_algorithm_parameter_given_algo_or_data_name(name)
    json_return = simplejson.dumps(parameters)

    return HttpResponse(json_return)

def user_uploaded_dataset(request):

    algo_name = request.GET['algo']
    data_name = request.GET['data']

    # get data path and load data
    now = datetime.datetime.now()
    if now.month < 10:
        mth = str(0)+str(now.month)
    else:
        mth = str(now.month)

    if now.day < 10:
        day = str(0)+str(now.day)
    else:
        day = str(now.day)

    path = '/static_media_clustapp/documents/'+str(now.year)+'/'+mth+'/'+day+'/'
    full_path = os.path.realpath('.')
    file_name = full_path+path+data_name
    data_file = scipy.io.loadmat(file_name)

    input_data = data_file['X']
    correct_label = data_file['y']

    # Calling Algorithms
    clustered_label = {}
    unique_label = {}
    if algo_name=="MiniBatchKMeans":
        print 'MiniBatchKMeans'
        kmean_label = algorithm_manager.call_kmean(2, input_data, True)
        clustered_label = kmean_label

    elif algo_name=="Spectral Clustering":
        print "Spectral Clustering"
        spectral_label = algorithm_manager.call_spectral(2, 'arpack', input_data, True)
        clustered_label = spectral_label

    elif algo_name=="Affinity Propagation":
        print "Affinity Propagation"
        affinity_label = algorithm_manager.call_affinity(0.9, input_data, True)
        clustered_label = affinity_label


    # saving the result in the correct directory
    output_data = {}
    output_data ['y'] = clustered_label
    out_file_name = full_path+path+data_name[:-4] + '_result.mat'
    data_file = scipy.io.savemat(out_file_name, output_data)

    # return the path
    return_file_name = path+data_name[:-4]  + '_result.mat'
    return HttpResponse(return_file_name)

def get_machine_learning_result_given_algorithm_and_dataset(request):
    algo_name = request.GET['algo']
    data_name = request.GET['data']

    print algo_name
    print data_name

    data_dict = {}
    input_data = None
    n_samples = 1500

    # Generateing Sample Data Algorithm
    from sklearn import cluster, datasets 
    if data_name=="Sample Blob":
        blob_dict, X, y = algorithm_manager.generate_blob_sample()
        data_dict = blob_dict
        input_data = X

    elif data_name=="Sample Circle":
        circle_dict,X,y = algorithm_manager.generate_circle_sample()
        #circle_dict,X,y = datasets.make_blobs(n_samples=n_samples, random_state=8)
        data_dict = circle_dict
        input_data = X

    elif data_name=="Sample Moon":
        moon_dict,X,y = algorithm_manager.generate_moon_sample()
        data_dict = moon_dict
        input_data = X

    clustered_label = {}
    unique_label = {}

    # Calling Algorithms
    if algo_name=="MiniBatchKMeans":
        print 'MiniBatchKMeans'
        kmean_label, unique_label = algorithm_manager.call_kmean(2, input_data, False)
        clustered_label = kmean_label

    elif algo_name=="Spectral Clustering":
        print "Spectral Clustering"
        spectral_label, unique_label = algorithm_manager.call_spectral(2, 'arpack', input_data, False)
        clustered_label = spectral_label

    elif algo_name=="Affinity Propagation":
        print "Affinity Propagation"
        affinity_label, unique_label = algorithm_manager.call_affinity(0.9, input_data, False)
        clustered_label = affinity_label

    elif algo_name=="Greedy":
        print "Greedy"
        greedy_label, unique_label = algorithm_manager.call_greedy(2, input_data, False)
        clustered_label = greedy_label

    # main return dictionary contain dictionary about everything
    return_dict = {}
    return_dict['original_data_points'] = data_dict
    return_dict['clustered_data_label'] = clustered_label
    return_dict['clustered_data_unique_label'] = unique_label
    json_return = simplejson.dumps(return_dict)


    return HttpResponse(json_return)

    # useless stuff
def fuck(request):
    return render_to_response(
            'engine/test_home.html',
            {
            }
    )