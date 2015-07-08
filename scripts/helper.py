"""Helper python script that complements the prepopulate script.

Assumes that the Django application has already been configured, so
that import commands can operate at the top of the file."""

from annis.models import AnnisServer
from texts.models import Corpus
from texts.models import HtmlVisualizationFormat
import xml.etree.ElementTree as ET
from urllib import request

def create_annis_server():
    """Creates default ANNIS server information."""
    try:
        annis = AnnisServer.objects.get(base_domain__exact=
                                        'https://corpling.uis.georgetown.edu')
    except AnnisServer.DoesNotExist:
        print("Saving a new instance of ANNIS Server")
        annis = AnnisServer.objects.create()
        annis.title = 'Georgetown Annis'
        annis.base_domain = 'https://corpling.uis.georgetown.edu'
        annis.corpus_metadata_url = "annis-service/annis/meta/corpus/:corpus_name"
        annis.corpus_docname_url = "annis-service/annis/meta/docnames/:corpus_name"
        annis.document_metadata_url = "annis-service/annis/meta/doc/:corpus_name/:document_name"
        annis.html_visualization_url = "annis/embeddedvis/htmldoc/:corpus_name/:document_name?config=:html_visualization_format"
        annis.save()

def load_known_corpora():
    """Defines known corpora in advance.

    For various reasons, we don't want to query the ANNIS server for available corpora:
    They're not ready for the URN resolver. Certain metadata about them isn't available
    from ANNIS, such as the urn_code."""

    print ("Loading Corpora")

    shenoute_a22 = Corpus()
    shenoute_a22.annis_corpus_name = "shenoute.a22"
    shenoute_a22.title = "Acephalous Work 22"
    shenoute_a22.slug = "acephalous_work_22"
    shenoute_a22.urn_code = "shenoute.a22"
    shenoute_a22.annis_code = "c2hlbm91dGUuYTIy"
    shenoute_a22.github = "https://github.com/CopticScriptorium/corpora/tree/master/shenoute-a22"

    patrum = Corpus()
    patrum.annis_corpus_name = "apophthegmata.patrum"
    patrum.title = "Apophthegmata Patrum"
    patrum.slug = "ap"
    patrum.urn_code = "ap"
    patrum.annis_code = "YXBvcGh0aGVnbWF0YS5wYXRydW0"
    patrum.github = "https://github.com/CopticScriptorium/corpora/tree/master/AP"

    saof = Corpus()
    saof.annis_corpus_name = "shenoute.abraham.our.father"
    saof.title = "Abraham Our Father"
    saof.slug = "abraham_our_father"
    saof.urn_code = "shenoute.abraham"
    saof.annis_code = "c2hlbm91dGUuYWJyYWhhbS5vdXIuZmF0aGVy"
    saof.github = "https://github.com/CopticScriptorium/corpora/tree/master/abraham"

    besa = Corpus()
    besa.annis_corpus_name = "besa.letters"
    besa.title = "Letter to Aphthonia"
    besa.slug = "to_aphthonia"
    besa.urn_code = "besa.aphthonia"
    besa.annis_code = "YmVzYS5sZXR0ZXJz"
    besa.github = "https://github.com/CopticScriptorium/corpora/tree/master/besa-letters"

    fox = Corpus()
    fox.annis_corpus_name = "shenoute.fox"
    fox.title = "Not Because a Fox Barks"
    fox.slug = "not_because_a_fox_barks"
    fox.urn_code = "shenoute.fox"
    fox.annis_code = "c2hlbm91dGUuZm94"
    fox.github = "https://github.com/CopticScriptorium/corpora/tree/master/shenoute-fox"

    mark = Corpus()
    mark.annis_corpus_name = "sahidica.mark"
    mark.title = "Gospel of Mark"
    mark.slug = "gospel_of_mark"
    mark.urn_code = "nt.mark"
    mark.annis_code = "c2FoaWRpY2EubWFyaw"
    mark.github = "https://github.com/CopticScriptorium/corpora/tree/master/bible"

    corinth = Corpus()
    corinth.annis_corpus_name = "sahidica.1corinthians"
    corinth.title = "1 Corinthians"
    corinth.slug = "1st_corinthians"
    corinth.urn_code = "nt.1cor"
    corinth.annis_code = "c2FoaWRpY2EuMWNvcmludGhpYW5z"
    corinth.github = "https://github.com/CopticScriptorium/corpora/tree/master/bible"

    snt = Corpus()
    snt.annis_corpus_name = "sahidica.nt"
    snt.title = "New Testament"
    snt.slug = "new-testament"
    snt.urn_code = "nt"
    snt.annis_code = "c2FoaWRpY2EubnQ"
    snt.github = "https://github.com/CopticScriptorium/corpora/tree/master/bible"

    eager = Corpus()
    eager.annis_corpus_name = "shenoute.eagerness"
    eager.title = "I See Your Eagerness"
    eager.slug = "eagernesss"
    eager.urn_code = "shenoute.eagerness"
    eager.annis_code = "c2hlbm91dGUuZWFnZXJuZXNz"
    eager.github = "https://github.com/CopticScriptorium/corpora/tree/master/shenoute-eagerness"

    known_corpora = [shenoute_a22, patrum, saof, besa, fox, mark, corinth, snt, eager]

    for one in known_corpora:
        try:
            Corpus.objects.get(annis_corpus_name__exact=one.annis_corpus_name)
        except Corpus.DoesNotExist:
            one.save()

def define_visualizations():
    """Unfortunately, these mappings are defined in the database, when they probably
    should be defined in code. This routine pre-populates the database with the expected
    visualizations."""

    norm = HtmlVisualizationFormat()
    norm.slug = "norm"
    norm.button_title = "normalized"
    norm.title = "Normalized Text"

    analytic = HtmlVisualizationFormat()
    analytic.slug = "analytic"
    analytic.button_title = "analytic"
    analytic.title = "Analytic Visualization"

    dipl = HtmlVisualizationFormat()
    dipl.slug = "dipl"
    dipl.button_title = "diplomatic"
    dipl.title = "Diplomatic Edition"

    sahidica = HtmlVisualizationFormat()
    sahidica.slug = "sahidica"
    sahidica.button_title = "chapter"
    sahidica.title = "Sahidica Chapter View"

    for vis in [norm, analytic, dipl, sahidica]:
        try:
            HtmlVisualizationFormat.objects.get(slug__exact=vis.slug)
        except HtmlVisualizationFormat.DoesNotExist:
            vis.save()

def find_corpora_visualizations():
    """Finds the visualizations for each corpora from ANNIS, and copies the data
    into the database for later reference."""

    # build a quick map of visualizations, so that we can reference by annis label.
    vis_map = dict()
    for vis in HtmlVisualizationFormat.objects.all():
        vis_map[vis.slug] = vis

    for corpus in Corpus.objects.all():
        # get the list of all the visualizations already loaded for this corpus.
        already_have = set()
        for one_fmt in corpus.html_visualization_formats.all():
            already_have.add(one_fmt.slug)

        url_fmt = "https://corpling.uis.georgetown.edu/annis-service/annis/query/resolver/{0}/NULL/node"
        url_to_fetch = url_fmt.format(corpus.annis_corpus_name)
        res = request.urlopen(url_to_fetch)
        root = ET.fromstring(res.read())
        xpath = "./resolverEntry[visType='htmldoc']/mappings/entry/value"
        added = False
        for one_node in root.findall(xpath):
            vis_slug = one_node.text
            if vis_slug not in already_have:
                corpus.html_visualization_formats.add(vis_map[vis_slug])
                added = True

        # If we added any visualizations, save them now
        if added:
            corpus.save()
