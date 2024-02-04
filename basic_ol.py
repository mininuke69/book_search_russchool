## using open library api
from requests import get
from json import dump

def sorter(d: dict):
    if d:
        return (
            d["author"],
            5.0 - d["rating"] if d["rating"] else 5.0,
            d["title"],
            d["rating_count"],
        )
    else:
        return ("z"*99, )


def fetch_book(q: str):
    global event
    author = q.split(" - ")[0].replace(" ", "+")
    title = q.split(" - ")[-1].removesuffix(".mobi\n").removesuffix(".mobi").replace(" ", " ")
    print(f'getting {title.rjust(50)}. {str(round(books.index(q) / len(books) * 100, 1)).ljust(5)}%. {event}', end="\r")
    response = get(f'https://openlibrary.org/search.json?q={author}-{title}').json()
    ratings = []
    for result in response["docs"]:
        try:
            ratings.append((result["ratings_count"], result["ratings_average"]))
        except KeyError:
            pass
    
    
    if ratings:
        rating_highest_count = sorted(ratings, reverse=True)[0]
        event = ''
        return {
            "author": author,
            "rating": rating_highest_count[1],
            "title": title,
            "rating_count": rating_highest_count[0]
        }
    else:
        event = f'no results for {title}'
        return {
            "author": author,
            "title": title,
            "rating": None,
            "rating_count": 0
        }




if __name__ == '__main__':
    event = ""
    with open("big.txt") as books_file:
        books = books_file.readlines()

    fetch_map = map(fetch_book, books)
    results = sorted(list(fetch_map), key=sorter)

    #print(results)
    with open("output_ol.json", "w") as output_ol_file:
        dump(results, output_ol_file)