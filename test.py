# test_recommender.py
from recommender.recommender import get_music_recommendations

tracks = get_music_recommendations("happy")
for t in tracks:
    print(f"{t['title']} by {t['artist']}")
    print(f"Preview: {t['preview_url']}\n")
