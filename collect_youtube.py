from collectors.youtube_collector import collect_multiple_queries, save_rows_to_csv
import os

API_KEY = "AIzaSyBSbq5iX74P5lHRrOiGhJ8WdSED3K0-Bso"


def main():
    
    #if not API_KEY:
       # raise ValueError ("API KEY NAO ENCOTRADA")
    
    queries = [
        # trap / rap geral
        "trap br type beat",
        "rap br type beat",
        "dark trap brasil",
        "underground trap brasil",

        # subgeneros
       # "pluggnb brasil",
        #"plug type beat brasil",
        #"detroit type beat brasil",
       # "drill type beat brasil",
       # "trapsoul type beat brasil",
        #"rnb trap brasil",

        # artistas BR
        "matuê type beat",
        "veigh type beat",
       # "yunk vino type beat",
        "teto type beat",
       # "kayblack type beat",
        "alee type beat",
       # "derek type beat",

        # artistas internacionais que influenciam a cena
        #"travis scott type beat",
       # "future type beat",
       # "playboi carti type beat",
        #"kanye west type beat"
    ]

    rows = collect_multiple_queries(
        api_key=API_KEY,
        queries=queries,
        max_pages=1,
    )
    
    if not rows:
        print("Nenhum dado coletado!")
        return 
    save_rows_to_csv(rows, "data/raw/youtube_music.csv")
    print(f"{len(rows)} linhas salvas em data/raw/youtube_music.csv")
    
if __name__ == "__main__":
    main()