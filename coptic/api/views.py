import logging
import json
from api.json import json_view
from api.encoder import encode_corpus, encode_text
from texts.models import Text, Corpus, TextMeta, SpecialMeta
import functools

log = logging.getLogger(__name__)
TEXT_PREFETCH_FIELDS = 'html_visualizations'
ALLOWED_MODELS = ('texts', 'corpus', 'urn')


@json_view()
def api(request, params):
    'Search with the search params from the client-side application'
    get = request.GET
    log.info('API called with %s, %s' % (request, params))

    return _query(_process_param_values(params.split("/"), get))


def _query(params):
    'Search and return data via the JSON API'

    objects = {}

    if 'model' in params:
        model = params['model']

        if model == 'urn' and 'urn' in params:
            _process_urn_request(params['urn'], objects)
        elif model == 'corpus':
            if 'filters' in params:
                corpus_ids, text_ids = _corpus_and_text_ids_from_filters(params['filters'])
                corpora = Corpus.objects.filter(id__in=set(corpus_ids))

                if text_ids:
                    _add_texts_to_corpora(corpora, text_ids)
                else:
                    _add_texts_to_corpora(corpora)

            else:  # There are no filters. Check for specific corpus.
                if 'corpus' in params and 'slug' in params['corpus']:
                    corpora = Corpus.objects.filter(slug=params['corpus']['slug'])
                else:
                    corpora = Corpus.objects.all()

                _add_texts_to_corpora(corpora)

            # fetch the results and add to the objects dict
            objects['corpus'] = _json_from_corpora(corpora)

        # Otherwise, if this is a query to the texts model
        elif model == 'texts':
            if 'corpus' in params and 'slug' in params['corpus'] and \
               'text'   in params and 'slug' in params['text']:
                corpus = Corpus.objects.get(slug=params['corpus']['slug'])
                text = Text.objects.filter(slug=params['text']['slug'], corpus=corpus.id).prefetch_related(TEXT_PREFETCH_FIELDS).first()
            else:
                objects['error'] = 'No Text Query specified--missing corpus slug or text slug'
                return objects

            # fetch the results and add to the objects dict
            objects['text'] = encode_text(text)

    # Otherwise, no query is specified
    else:
        objects['error'] = 'No Query specified'

    return objects


def _process_urn_request(urn, objects):
    texts = texts_for_urn(urn)

    # Find the corpora containing the matching texts
    corpus_ids = set([text.corpus_id for text in texts])
    corpora = Corpus.objects.filter(id__in=corpus_ids)

    _add_texts_to_corpora(corpora, texts=texts)
    objects['corpus'] = _json_from_corpora(corpora)


def texts_for_urn(urn):
    # Find texts matching the URN using their metadata
    matching_tm_ids = TextMeta.objects.filter(name='document_cts_urn', value__iregex='^' + urn + r'($|[\.:])'
    	).values_list('id', flat=True)
    texts = Text.objects.filter(text_meta__name='document_cts_urn',
        text_meta__id__in=matching_tm_ids).order_by('slug')
    return texts


def _add_texts_to_corpora(corpora, text_ids=None, texts=None):
    adding_texts = texts if texts else \
		(Text.objects.filter(id__in=text_ids) if text_ids else Text.objects.all()).\
        select_related('corpus').order_by('slug')
    texts_by_id = {t.id: t for t in adding_texts}

    def create_order(title, order):
        'order should be a list of zero or one element containing a string'
        if order and len(order) == 1:
            return order[0]

        return title

    text_ids_and_orders = [(text.id, create_order(text.title, [o.value for o in text.text_meta.filter(name='order')]))
                           for text in adding_texts]  # List of id, order tuples
    sorted_text_ids_and_orders = sorted(text_ids_and_orders, key=lambda t: t[1])
    sorted_text_ids = [tio[0] for tio in sorted_text_ids_and_orders]
    for corpus in corpora:
        corpus.texts = [texts_by_id[i] for i in sorted_text_ids if texts_by_id[i].corpus_id == corpus.id]


def _corpus_and_text_ids_from_filters(filters):
    splittable = [sm.name for sm in SpecialMeta.objects.all() if sm.splittable]
    corpus_ids_by_field = {}
    text_ids_by_field = {}

    for filter in filters:
        name  = filter['field']
        value = filter['filter']
        corpus_ids = corpus_ids_by_field.get(name, set())
        text_ids   = text_ids_by_field  .get(name, set())

        partly_filtered = Text.objects.filter(text_meta__name__iexact=name)
        texts = partly_filtered.filter(text_meta__value__contains=value) if name in splittable else \
			partly_filtered.filter(text_meta__value__iexact=value)

        text_ids  .update([t.id        for t in texts])
        corpus_ids.update([t.corpus_id for t in texts])

        if corpus_ids:
            corpus_ids_by_field[name] = corpus_ids
        if text_ids:
            text_ids_by_field[name] = text_ids

    return _intersect_ids_across_fields(corpus_ids_by_field), _intersect_ids_across_fields(text_ids_by_field)


def _intersect_ids_across_fields(id_sets_by_fieldname):
	ids_sets = [id_set for id_set in id_sets_by_fieldname.values()]

	def intersect_sets(set1, set2):
		'Intersect IDs in successive sets to ensure the remaining IDs are in all sets'
		intersection = set1 & set2
		log.debug('Intersection of %s and %s is %s' % (set1, set2, intersection))
		return intersection

	return functools.reduce(intersect_sets, ids_sets) if ids_sets else []


def _json_from_corpora(queryset):
    return [encode_corpus(item) for item in queryset]


def _process_param_values(params, query_dict):
    'Process the param values to improve security'
    clean = {}

    if query_dict:
        # first, process the type of query by model or manifest
        if 'model' in query_dict:
            if query_dict['model'] in ALLOWED_MODELS:
                clean['model'] = query_dict['model']

            if 'corpus_slug' in query_dict:
                clean['corpus'] = {
                    'slug': query_dict['corpus_slug'].strip()
                }

            if 'text_slug' in query_dict:
                clean['text'] = {
                    'slug': query_dict['text_slug'].strip()
                }

            if 'urn_value' in query_dict:
                clean['urn'] = query_dict['urn_value'].strip()

        # Then process the supplied query
        filters = [json.loads(filter) for filter in query_dict.getlist('filters')]
        if filters:
            clean['filters'] = filters

    else:
        if 'manifest' in params:
            clean['manifest'] = True

        elif 'urns' in params:
            clean['urns'] = True

    return clean
