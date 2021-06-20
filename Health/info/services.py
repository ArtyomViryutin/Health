from .models import Disease, Criteria, Code


def clear_tables(models):
    for model in models:
        model.objects.all().delete()


def create_disease(**kwargs):
    return Disease.objects.create(**kwargs)


def create_code(**kwargs):
    return Code.objects.create(**kwargs)


def create_criteria(criteria, disease):
    try:
        obj = Criteria.objects.get(criteria=criteria)
    except Criteria.DoesNotExist:
        obj = Criteria.objects.create(criteria=criteria)
    obj.diseases.add(disease)


def bulk_codes_create(codes, disease):
    return Code.objects.bulk_create([Code(code=code, disease=disease) for code in codes])


# data: list: {criteria: list, codes: list, description: str}
def update_database(data):
    clear_tables([Disease, Criteria, Code])
    for item in data:
        criteria, codes, description, name = item.get('criteria'), item.get('codes'), \
                                             item.get('description'), item.get('name')
        print(f'{"*" * 10}: {codes}', codes[0][0] == 'К', name)
        disease = create_disease(name=name, description=description)
        bulk_codes_create(codes, disease)
        for cr in criteria:
            create_criteria(cr, disease)



