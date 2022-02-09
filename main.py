from maps_api.geocoder import get_ll_spn, show_map


toponym_to_find = "Пермь, Ветлужская 89" #sys.argv[1:])

ll, spn = get_ll_spn(toponym_to_find)
show_map(ll, spn, add_params={"pt": f"{ll},pm2rdm"})
