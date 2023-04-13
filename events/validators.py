from datetime import datetime


def validate_search_by_date(search):
    formats = [
        '%d/%m/%Y', '%d/%m', '%m/%d/', '%Y/%m/%d', '%d/%m/%y'
    ]
    
    for f in formats:
        try:
            date = datetime.strptime(search, f)
            if f == '%d/%m' or f == '%m/%d/': 
                date = date.replace(year=datetime.now().year)
            print(date, "CONVERTIDA !")
            return date
        
        except Exception as error: print(error)
    
    return search


def validate_search_date_interval(search):
    search = search.split()
    if len(search) < 2: return
    
    start = validate_search_by_date(search[0])
    end = validate_search_by_date(search[1])
    if not (isinstance(start, datetime) and isinstance(end, datetime)):
        return None
    
    return start, end
