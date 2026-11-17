# Lightweight seed dataset for immediate availability
SEED_QA_PAIRS = [
    ("Who was the first President of the United States?", "George Washington", "politician", "George Washington", "George Washington was the first President of the United States, serving from 1789 to 1797."),
    ("Who is the current President of France?", "Emmanuel Macron", "politician", "Emmanuel Macron", "Emmanuel Macron has been serving as President of France since 2017."),
    ("Which British Prime Minister led the country during World War II?", "Winston Churchill", "politician", "Winston Churchill", "Winston Churchill served as Prime Minister during most of World War II."),
    ("Who was the longest-serving US President?", "Franklin D. Roosevelt", "politician", "Franklin D. Roosevelt", "FDR served as President for over 12 years from 1933 until 1945."),
    ("Who holds the record for most Olympic gold medals?", "Michael Phelps", "athlete", "Michael Phelps", "Michael Phelps won 23 Olympic gold medals in swimming."),
    ("Which tennis player has won the most Grand Slam singles titles?", "Novak Djokovic", "athlete", "Novak Djokovic", "Novak Djokovic has won 24 Grand Slam singles titles."),
    ("Who is considered the greatest basketball player of all time?", "Michael Jordan", "athlete", "Michael Jordan", "Michael Jordan won 6 NBA championships with the Chicago Bulls."),
    ("Who holds the world record in the 100-meter sprint?", "Usain Bolt", "athlete", "Usain Bolt", "Usain Bolt set the world record of 9.58 seconds in 2009."),
    ("What is the largest country in the world by land area?", "Russia", "country", "Russia", "Russia covers over 17 million square kilometers."),
    ("What is the most populous country in the world?", "India", "country", "India", "India is the most populous country in the world."),
    ("What is the capital of Australia?", "Canberra", "city", "Canberra", "Canberra is the capital city of Australia, not Sydney or Melbourne."),
    ("Which city is known as the Big Apple?", "New York City", "city", "New York City", "New York City earned this nickname in the 1920s."),
    ("Which city is home to the Eiffel Tower?", "Paris", "city", "Paris", "The Eiffel Tower was built in Paris for the 1889 World's Fair."),
    ("Which scientist developed the theory of relativity?", "Albert Einstein", "historicalfigure", "Albert Einstein", "Einstein published his theory of relativity in the early 20th century."),
    ("Who was the first person to walk on the moon?", "Neil Armstrong", "historicalfigure", "Neil Armstrong", "Armstrong stepped on the moon on July 20, 1969."),
    ("Which inventor created the practical light bulb?", "Thomas Edison", "historicalfigure", "Thomas Edison", "Edison developed the first practical incandescent light bulb."),
    ("Who discovered penicillin?", "Alexander Fleming", "scientist", "Alexander Fleming", "Fleming discovered penicillin in 1928, revolutionizing medicine."),
    ("What is the speed of light in vacuum?", "299,792 km/s", "science", "Physics", "The speed of light in vacuum is approximately 300,000 kilometers per second."),
    ("What is the closest planet to the Sun?", "Mercury", "science", "Solar System", "Mercury orbits closest to the Sun."),
    ("Who founded Microsoft?", "Bill Gates and Paul Allen", "company", "Microsoft", "Bill Gates and Paul Allen founded Microsoft in 1975.")
]

def auto_seed_if_empty(db_manager):
    """Populates basic seed questions if database has 0 pairs, without heavy embeddings."""
    try:
        from database import QAPair
        stats = db_manager.get_dataset_stats()
        if stats.get("total_pairs", 0) == 0:
            for q, a, topic, example, explanation in SEED_QA_PAIRS:
                qa_pair = QAPair(
                    topic=topic,
                    example=example,
                    question=q,
                    answer=a,
                    explanation=explanation
                )
                db_manager.save_qa_pair(qa_pair)
    except Exception as e:
        pass
