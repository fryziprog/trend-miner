from collectors.youtube_collector import collect_multiple_queries, save_rows_to_csv


API_KEY = "AIzaSyCA88U8hM9ZOOpcJo35YqcRWS6Ao1xGKYw"


def main():
    queries = [
        "dark trap",
        "pluggnb",
        "type beat",
        "travis scott type beat",
        "brazilian trap",
        "rage beat",
    ]

    rows = collect_multiple_queries(
        api_key=API_KEY,
        queries=queries,
        max_pages=5,
    )

    save_rows_to_csv(rows, "data/raw/youtube_music.csv")
    print(f"{len(rows)} linhas salvas em data/raw/youtube_music.csv")


if __name__ == "__main__":
    main()