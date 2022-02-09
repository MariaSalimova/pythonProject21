from maps_api.geocoder import get_ll_spn, get_nearest_object, show_map


toponym_to_find = "Пермь, Ветлужская 89" #sys.argv[1:])

ll, spn = get_ll_spn(toponym_to_find)
response = get_nearest_object(ll, spn)
show_map(response)
