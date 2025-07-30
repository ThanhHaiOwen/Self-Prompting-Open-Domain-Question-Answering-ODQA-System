#!/usr/bin/env python3
"""
Script to create comprehensive sample data for the Self-Prompting ODQA System
"""

import sys
sys.path.append('.')
from database import DatabaseManager, QAPair

def create_comprehensive_dataset():
    """Create a comprehensive dataset with QA pairs across multiple topics"""
    
    # Initialize database
    db = DatabaseManager()
    
    # Comprehensive QA pairs across different topics
    sample_data = [
        # Politicians
        QAPair(
            topic='politician',
            example='Joe Biden',
            passage='Joe Biden is the 46th President of the United States, serving since January 20, 2021. He previously served as Vice President under Barack Obama from 2009 to 2017 and as a U.S. Senator from Delaware from 1973 to 2009.',
            entity='Joe Biden',
            question='Who is the current President of the United States?',
            answer='Joe Biden',
            explanation='Joe Biden became the 46th President of the United States on January 20, 2021, and is currently serving in that role.'
        ),
        QAPair(
            topic='politician',
            example='Winston Churchill',
            passage='Winston Churchill was a British statesman who served as Prime Minister of the United Kingdom from 1940 to 1945 and again from 1951 to 1955. He led Britain during World War II and is known for his inspiring speeches and leadership during the war.',
            entity='Winston Churchill',
            question='Who was the British Prime Minister during World War II?',
            answer='Winston Churchill',
            explanation='Winston Churchill served as British Prime Minister from 1940 to 1945, leading the country through most of World War II with his inspiring leadership and speeches.'
        ),
        QAPair(
            topic='politician',
            example='Nelson Mandela',
            passage='Nelson Mandela was a South African anti-apartheid revolutionary and political leader who served as President of South Africa from 1994 to 1999. He was imprisoned for 27 years for his activism and became a symbol of resistance against apartheid.',
            entity='Nelson Mandela',
            question='Who was the first Black president of South Africa?',
            answer='Nelson Mandela',
            explanation='Nelson Mandela became the first Black president of South Africa in 1994, serving until 1999, after spending 27 years in prison for his anti-apartheid activism.'
        ),
        
        # Scientists
        QAPair(
            topic='scientist',
            example='Marie Curie',
            passage='Marie Curie was a Polish-French physicist and chemist who conducted pioneering research on radioactivity. She was the first woman to win a Nobel Prize and the only person to win Nobel Prizes in two different scientific fields (Physics in 1903 and Chemistry in 1911).',
            entity='Marie Curie',
            question='Who was the first woman to win a Nobel Prize?',
            answer='Marie Curie',
            explanation='Marie Curie was the first woman to win a Nobel Prize, receiving the Nobel Prize in Physics in 1903 for her research on radioactivity, and later won the Nobel Prize in Chemistry in 1911.'
        ),
        QAPair(
            topic='scientist',
            example='Charles Darwin',
            passage='Charles Darwin was an English naturalist who proposed the theory of evolution through natural selection. His book On the Origin of Species published in 1859 revolutionized biology and our understanding of life on Earth.',
            entity='Charles Darwin',
            question='Who proposed the theory of evolution through natural selection?',
            answer='Charles Darwin',
            explanation='Charles Darwin proposed the theory of evolution through natural selection in his groundbreaking book On the Origin of Species published in 1859.'
        ),
        QAPair(
            topic='scientist',
            example='Isaac Newton',
            passage='Isaac Newton was an English mathematician, physicist, and astronomer who formulated the laws of motion and universal gravitation. His work Principia Mathematica published in 1687 laid the foundations for classical mechanics.',
            entity='Isaac Newton',
            question='Who formulated the laws of motion and universal gravitation?',
            answer='Isaac Newton',
            explanation='Isaac Newton formulated the fundamental laws of motion and universal gravitation, publishing his groundbreaking work in Principia Mathematica in 1687.'
        ),
        
        # Countries
        QAPair(
            topic='country',
            example='Japan',
            passage='Japan is an island nation in East Asia consisting of four main islands: Honshu, Hokkaido, Kyushu, and Shikoku. Its capital and largest city is Tokyo, and the country is known for its rich culture, technology, and cuisine.',
            entity='Tokyo',
            question='What is the capital of Japan?',
            answer='Tokyo',
            explanation='Tokyo is the capital and largest city of Japan, serving as the political, economic, and cultural center of the country.'
        ),
        QAPair(
            topic='country',
            example='Brazil',
            passage='Brazil is the largest country in South America and the fifth-largest country in the world by area. Its capital is Brasilia, and it is famous for the Amazon rainforest, Rio de Janeiro, and its vibrant culture including samba and carnival.',
            entity='Brasilia',
            question='What is the capital of Brazil?',
            answer='Brasilia',
            explanation='Brasilia is the capital of Brazil, a planned city that was built in the 1950s and became the capital in 1960, replacing Rio de Janeiro.'
        ),
        QAPair(
            topic='country',
            example='Australia',
            passage='Australia is a country and continent surrounded by the Indian and Pacific oceans. Its capital is Canberra, though Sydney is its largest city. Australia is known for its unique wildlife, including kangaroos and koalas, and the Great Barrier Reef.',
            entity='Canberra',
            question='What is the capital of Australia?',
            answer='Canberra',
            explanation='Canberra is the capital of Australia, located between Sydney and Melbourne, and serves as the seat of the Australian government.'
        ),
        
        # Historical Figures
        QAPair(
            topic='historical_figure',
            example='Leonardo da Vinci',
            passage='Leonardo da Vinci was an Italian Renaissance polymath who excelled in art, science, engineering, and invention. He painted the Mona Lisa and The Last Supper, and designed flying machines, tanks, and anatomical studies centuries ahead of his time.',
            entity='Leonardo da Vinci',
            question='Who painted the Mona Lisa?',
            answer='Leonardo da Vinci',
            explanation='Leonardo da Vinci painted the Mona Lisa during the Italian Renaissance, creating one of the most famous and recognizable paintings in the world.'
        ),
        QAPair(
            topic='historical_figure',
            example='Cleopatra',
            passage='Cleopatra VII was the last active pharaoh of Ancient Egypt, ruling from 51 to 30 BCE. She was known for her intelligence, political acumen, and relationships with Julius Caesar and Mark Antony of Rome.',
            entity='Cleopatra',
            question='Who was the last pharaoh of Ancient Egypt?',
            answer='Cleopatra',
            explanation='Cleopatra VII was the last active pharaoh of Ancient Egypt, ruling until 30 BCE when Egypt became a Roman province.'
        ),
        
        # Geography
        QAPair(
            topic='geography',
            example='Mount Everest',
            passage='Mount Everest is the highest mountain in the world, standing at 8,848.86 meters (29,031.7 feet) above sea level. It is located in the Himalayas on the border between Nepal and Tibet, and is known as Sagarmatha in Nepali and Chomolungma in Tibetan.',
            entity='Mount Everest',
            question='What is the highest mountain in the world?',
            answer='Mount Everest',
            explanation='Mount Everest is the highest mountain in the world at 8,848.86 meters above sea level, located in the Himalayas between Nepal and Tibet.'
        ),
        QAPair(
            topic='geography',
            example='Amazon River',
            passage='The Amazon River is the longest river in the world, flowing approximately 6,400 kilometers through South America. It originates in the Peruvian Andes and flows through Brazil before emptying into the Atlantic Ocean.',
            entity='Amazon River',
            question='What is the longest river in the world?',
            answer='Amazon River',
            explanation='The Amazon River is the longest river in the world, stretching approximately 6,400 kilometers from the Peruvian Andes to the Atlantic Ocean in Brazil.'
        ),
        
        # Literature
        QAPair(
            topic='literature',
            example='William Shakespeare',
            passage='William Shakespeare was an English playwright and poet widely regarded as the greatest writer in the English language. He wrote approximately 39 plays and 154 sonnets, including famous works like Hamlet, Romeo and Juliet, and Macbeth.',
            entity='William Shakespeare',
            question='Who wrote Romeo and Juliet?',
            answer='William Shakespeare',
            explanation='William Shakespeare wrote Romeo and Juliet, one of his most famous tragedies about young star-crossed lovers, written in the early part of his career.'
        ),
        
        # Technology
        QAPair(
            topic='technology',
            example='Tim Berners-Lee',
            passage='Tim Berners-Lee is a British computer scientist who invented the World Wide Web in 1989 while working at CERN. He created the first web browser, web server, and website, fundamentally changing how information is shared globally.',
            entity='Tim Berners-Lee',
            question='Who invented the World Wide Web?',
            answer='Tim Berners-Lee',
            explanation='Tim Berners-Lee invented the World Wide Web in 1989 while working at CERN, creating the foundation for the modern internet as we know it today.'
        )
    ]
    
    return sample_data, db

if __name__ == "__main__":
    sample_data, db = create_comprehensive_dataset()
    
    # Insert all sample data
    inserted_count = 0
    for qa_pair in sample_data:
        try:
            qa_id = db.save_qa_pair(qa_pair)
            print(f'Inserted QA pair {inserted_count + 1}: {qa_pair.question[:50]}... (ID: {qa_id})')
            inserted_count += 1
        except Exception as e:
            print(f'Error inserting QA pair: {e}')
    
    print(f'\n✅ Successfully inserted {inserted_count} new QA pairs!')
    all_pairs = db.get_qa_pairs()
    print(f'Total QA pairs in database: {len(all_pairs)}')
