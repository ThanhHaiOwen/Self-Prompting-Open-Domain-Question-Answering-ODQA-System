#!/usr/bin/env python3
"""
Eliminate ALL formulaic questions and replace with authentic, diverse questions
"""

import sys
sys.path.append('.')
from database import DatabaseManager, QAPair

def identify_and_remove_formulaic_questions():
    """Identify and remove all formulaic questions from database"""
    db = DatabaseManager()
    all_pairs = db.get_qa_pairs()
    
    formulaic_patterns = [
        'What is significant about Geographic Feature',
        'What contributions did Literary Figure',
        'What type of discoveries did Scientist',
        'What was Politician Figure',
        'What makes Country',
        'What impact did Tech Innovation',
        'What role did Historical Figure',
        'How did', 'influence', 'field',  # Generic patterns
        'made significant contributions',
        'important aspect of',
        'represents an important',
        'demonstrates natural processes'
    ]
    
    formulaic_ids = []
    authentic_count = 0
    
    for pair in all_pairs:
        is_formulaic = False
        
        # Check if question or answer contains formulaic patterns
        for pattern in formulaic_patterns:
            if (pattern in pair.question or 
                pattern in pair.answer or 
                pattern in pair.explanation or
                'Figure' in pair.example or
                'Innovation' in pair.example or
                'Feature' in pair.example):
                is_formulaic = True
                break
        
        if is_formulaic:
            formulaic_ids.append(pair.id)
        else:
            authentic_count += 1
    
    print(f"Found {len(formulaic_ids)} formulaic questions to remove")
    print(f"Keeping {authentic_count} authentic questions")
    
    # Remove formulaic questions
    for qa_id in formulaic_ids:
        try:
            # Note: We'll need to implement a delete method or clear and rebuild
            pass
        except Exception as e:
            print(f"Error removing question {qa_id}: {e}")
    
    return len(formulaic_ids), authentic_count

def create_authentic_geography_questions():
    """Create 50+ authentic geography questions based on real geographical facts"""
    return [
        # Mountain Ranges & Peaks
        QAPair(topic='geography', example='K2', passage='K2, the second-highest mountain in the world at 8,611 meters, is considered more dangerous to climb than Mount Everest. It has a fatality rate of about 25% compared to Everest\'s 4%. K2 has never been climbed in winter until 2021. The mountain is located on the border between Pakistan and China and is known as the "Savage Mountain."', entity='25% fatality rate', question='What is K2\'s fatality rate compared to Mount Everest?', answer='about 25% compared to Everest\'s 4%', explanation='K2 has a much higher fatality rate of about 25% compared to Mount Everest\'s 4%, making it more dangerous to climb.'),
        
        QAPair(topic='geography', example='Denali', passage='Denali in Alaska is the tallest mountain in North America at 6,190 meters. It was formerly known as Mount McKinley until 2015 when it was officially renamed to its original Native Alaskan name. The mountain has the largest base-to-peak rise of any mountain on Earth at 5,500 meters. Temperatures can drop to -40°C even in summer.', entity='largest base-to-peak rise', question='What unique measurement record does Denali hold among world mountains?', answer='largest base-to-peak rise on Earth', explanation='Denali has the largest base-to-peak rise of any mountain on Earth at 5,500 meters.'),
        
        QAPair(topic='geography', example='Matterhorn', passage='The Matterhorn on the Swiss-Italian border is one of the most photographed mountains in the world due to its distinctive pyramid shape. It was one of the last major Alpine peaks to be climbed, first summited in 1865. Four of the seven climbers died on the descent during the first successful ascent. The mountain appears on Toblerone chocolate packaging.', entity='four climbers died on descent', question='What tragedy occurred during the Matterhorn\'s first successful ascent in 1865?', answer='four of seven climbers died on the descent', explanation='During the first successful ascent of the Matterhorn in 1865, four of the seven climbers died on the descent.'),
        
        # Ocean Features & Phenomena
        QAPair(topic='geography', example='Bermuda Triangle', passage='The Bermuda Triangle covers approximately 500,000 square miles of ocean between Florida, Bermuda, and Puerto Rico. Despite popular myths, the U.S. Coast Guard and Lloyd\'s of London report no more incidents in this area than anywhere else. The area experiences rapid weather changes and has some of the deepest underwater trenches in the world.', entity='no more incidents than elsewhere', question='What do official records show about incident rates in the Bermuda Triangle?', answer='no more incidents than anywhere else', explanation='The U.S. Coast Guard and Lloyd\'s of London report that the Bermuda Triangle has no more incidents than any other heavily traveled area of ocean.'),
        
        QAPair(topic='geography', example='Ring of Fire', passage='The Pacific Ring of Fire contains 75% of the world\'s active volcanoes and experiences 90% of the world\'s earthquakes. It stretches 40,000 kilometers around the Pacific Ocean. The ring is caused by tectonic plate movements and subduction zones. Indonesia has the most active volcanoes in the Ring of Fire with 130 active volcanoes.', entity='90% of earthquakes', question='What percentage of the world\'s earthquakes occur in the Pacific Ring of Fire?', answer='90%', explanation='The Pacific Ring of Fire experiences 90% of the world\'s earthquakes due to intense tectonic activity.'),
        
        QAPair(topic='geography', example='Mid-Atlantic Ridge', passage='The Mid-Atlantic Ridge is the longest mountain range on Earth at 65,000 kilometers, though most of it is underwater. It separates the Eurasian and North American plates in the north, and the African and South American plates in the south. Iceland sits directly on the ridge, which is why it has so much geothermal activity. The ridge spreads at about 2.5 cm per year.', entity='longest mountain range 65,000 km', question='What is the longest mountain range on Earth and how long is it?', answer='Mid-Atlantic Ridge at 65,000 kilometers', explanation='The Mid-Atlantic Ridge is the longest mountain range on Earth at 65,000 kilometers, though most of it is underwater.'),
        
        # Desert Phenomena
        QAPair(topic='geography', example='Atacama Desert', passage='The Atacama Desert in Chile is the driest non-polar desert in the world, with some weather stations never recording rainfall. Some areas haven\'t received rain for over 400 years. Despite this, the desert supports life including flamingos in salt lakes. NASA tests Mars rovers here because conditions are so similar to Mars.', entity='no rain for 400 years', question='How long have some areas of the Atacama Desert gone without rainfall?', answer='over 400 years', explanation='Some areas of the Atacama Desert haven\'t received rain for over 400 years, making it the driest non-polar desert.'),
        
        QAPair(topic='geography', example='Namib Desert', passage='The Namib Desert is considered the oldest desert in the world, existing for at least 55 million years. It contains some of the world\'s tallest sand dunes, reaching heights of 325 meters. The desert meets the Atlantic Ocean, creating a unique ecosystem where desert-adapted elephants and lions survive. Fog from the ocean provides the primary source of water for many organisms.', entity='oldest desert 55 million years', question='How old is the Namib Desert, making it the world\'s oldest?', answer='at least 55 million years', explanation='The Namib Desert is considered the oldest desert in the world, existing for at least 55 million years.'),
        
        # Unique Geological Formations
        QAPair(topic='geography', example='Giant\'s Causeway', passage='The Giant\'s Causeway in Northern Ireland consists of about 40,000 interlocking basalt columns formed by volcanic activity 50-60 million years ago. The columns are mostly hexagonal and fit together so perfectly they look man-made. Legend says it was built by giants, but it\'s actually the result of rapid cooling of lava. It\'s a UNESCO World Heritage Site.', entity='40,000 basalt columns', question='How many basalt columns make up the Giant\'s Causeway?', answer='about 40,000', explanation='The Giant\'s Causeway consists of about 40,000 interlocking basalt columns formed by ancient volcanic activity.'),
        
        QAPair(topic='geography', example='Devils Tower', passage='Devils Tower in Wyoming rises 386 meters above the surrounding terrain and was the first U.S. National Monument, designated in 1906. It\'s a volcanic neck formed by magma that cooled underground and was later exposed by erosion. The tower has vertical cracks that make it popular with rock climbers. Native American tribes consider it sacred and call it Bear Lodge.', entity='first National Monument 1906', question='What historic designation did Devils Tower receive in 1906?', answer='first U.S. National Monument', explanation='Devils Tower was designated as the first U.S. National Monument in 1906.'),
        
        # Cave Systems
        QAPair(topic='geography', example='Mammoth Cave', passage='Mammoth Cave in Kentucky is the world\'s longest known cave system with over 640 kilometers of surveyed passageways. New passages are still being discovered regularly. The cave system formed in limestone over millions of years. It\'s home to over 130 species, including 14 species of blind cave fish and other creatures that have adapted to permanent darkness.', entity='640 kilometers surveyed', question='How many kilometers of passageways have been surveyed in Mammoth Cave?', answer='over 640 kilometers', explanation='Mammoth Cave has over 640 kilometers of surveyed passageways, making it the world\'s longest known cave system.'),
        
        QAPair(topic='geography', example='Son Doong Cave', passage='Son Doong Cave in Vietnam is the world\'s largest cave passage by volume. It\'s so large that it could fit a 40-story skyscraper inside it. The cave contains enormous stalagmites up to 80 meters tall and has its own jungle and weather system. It was only discovered in 2009 and opened to limited tourism in 2013. Only 1,000 people are allowed to visit per year.', entity='fit 40-story skyscraper', question='How large is Son Doong Cave in terms of what could fit inside it?', answer='could fit a 40-story skyscraper', explanation='Son Doong Cave is so large that it could fit a 40-story skyscraper inside it, making it the world\'s largest cave passage by volume.'),
        
        # Extreme Weather Locations
        QAPair(topic='geography', example='Death Valley', passage='Death Valley holds the world record for the highest air temperature at 54.4°C (129.9°F) recorded on July 10, 1913. The valley is 282 feet below sea level at its lowest point called Badwater Basin. Despite its name, Death Valley supports over 1,000 species of plants and animals. It receives less than 5 cm of rainfall per year.', entity='54.4°C world record', question='What is the highest air temperature ever recorded and where?', answer='54.4°C in Death Valley', explanation='Death Valley holds the world record for highest air temperature at 54.4°C (129.9°F) recorded on July 10, 1913.'),
        
        QAPair(topic='geography', example='Mount Washington', passage='Mount Washington in New Hampshire recorded the highest surface wind speed ever measured at 372 km/h (231 mph) in 1934. The mountain experiences some of the world\'s most severe weather despite being only 1,916 meters tall. It has an alpine climate similar to northern Labrador. The weather changes so rapidly that it can go from calm to life-threatening in minutes.', entity='372 km/h wind speed', question='What is the highest surface wind speed ever recorded and where?', answer='372 km/h on Mount Washington', explanation='Mount Washington recorded the highest surface wind speed ever measured at 372 km/h (231 mph) in 1934.'),
        
        # Unique Water Bodies
        QAPair(topic='geography', example='Lake Hillier', passage='Lake Hillier in Australia is bright pink due to algae, bacteria, and high salt content. The lake maintains its pink color year-round and even when water is removed from the lake. It\'s about 600 meters long and surrounded by eucalyptus forest. The pink color is most vivid when viewed from above. Swimming is safe but not recommended due to the high salt content.', entity='bright pink year-round', question='What unusual characteristic does Lake Hillier in Australia maintain year-round?', answer='bright pink color', explanation='Lake Hillier maintains its bright pink color year-round due to algae, bacteria, and high salt content.'),
        
        QAPair(topic='geography', example='Lake Natron', passage='Lake Natron in Tanzania has a pH level as high as 10.5, making it almost as alkaline as ammonia. The lake can reach temperatures of 60°C (140°F). Animals that die in the lake become calcified and preserved like statues. Despite the harsh conditions, it\'s the only breeding ground for East Africa\'s lesser flamingos. The lake\'s red color comes from salt-loving microorganisms.', entity='pH 10.5 like ammonia', question='How alkaline is Lake Natron compared to common substances?', answer='pH 10.5, almost as alkaline as ammonia', explanation='Lake Natron has a pH level as high as 10.5, making it almost as alkaline as ammonia.'),
        
        # Tectonic Phenomena
        QAPair(topic='geography', example='San Andreas Fault', passage='The San Andreas Fault in California is 1,300 kilometers long and marks the boundary between the Pacific and North American tectonic plates. The fault moves about 5 cm per year on average. Scientists predict a major earthquake (magnitude 7.0 or higher) has a 60% probability of occurring along the fault in the next 30 years. The fault is visible from space.', entity='60% probability in 30 years', question='What is the probability of a major earthquake on the San Andreas Fault in the next 30 years?', answer='60%', explanation='Scientists predict a major earthquake (magnitude 7.0 or higher) has a 60% probability of occurring along the San Andreas Fault in the next 30 years.'),
        
        QAPair(topic='geography', example='East African Rift', passage='The East African Rift is slowly splitting Africa into two continents at a rate of 6-7 mm per year. In about 10 million years, the eastern part of Africa will separate completely. The rift has created a chain of lakes including Lake Victoria, Lake Tanganyika, and Lake Malawi. The rift is also where many early human fossils have been found, including "Lucy."', entity='splitting at 6-7 mm per year', question='How fast is the East African Rift splitting Africa apart?', answer='6-7 mm per year', explanation='The East African Rift is slowly splitting Africa into two continents at a rate of 6-7 mm per year.'),
        
        # Glacial Features
        QAPair(topic='geography', example='Lambert Glacier', passage='Lambert Glacier in Antarctica is the world\'s largest glacier, measuring about 100 kilometers wide and 400 kilometers long. It drains about 8% of the East Antarctic Ice Sheet. The glacier moves at about 400 meters per year toward the ocean. If all of Antarctica\'s ice melted, global sea levels would rise by about 60 meters.', entity='100 km wide, 400 km long', question='What are the dimensions of Lambert Glacier, the world\'s largest?', answer='100 kilometers wide and 400 kilometers long', explanation='Lambert Glacier is the world\'s largest glacier, measuring about 100 kilometers wide and 400 kilometers long.'),
        
        QAPair(topic='geography', example='Perito Moreno Glacier', passage='Perito Moreno Glacier in Argentina is one of the few glaciers in the world that is still advancing rather than retreating. The glacier advances about 2 meters per day at its center. It regularly calves icebergs into Lago Argentino with thunderous crashes. The glacier is about 250 square kilometers in area and 74 meters high at its terminus.', entity='advancing 2 meters per day', question='How fast does Perito Moreno Glacier advance daily?', answer='about 2 meters per day', explanation='Perito Moreno Glacier advances about 2 meters per day at its center, making it one of the few advancing glaciers.'),
        
        # Coral Reefs & Marine Features
        QAPair(topic='geography', example='Belize Barrier Reef', passage='The Belize Barrier Reef is the second-largest coral reef system in the world, stretching 300 kilometers along Belize\'s coast. It\'s home to 70 hard coral species, 36 soft coral species, and hundreds of invertebrate species. The reef includes the famous Blue Hole, a circular sinkhole 300 meters across and 125 meters deep. Charles Darwin described it as "the most remarkable reef in the West Indies."', entity='300 meters across, 125 meters deep', question='What are the dimensions of the Blue Hole in the Belize Barrier Reef?', answer='300 meters across and 125 meters deep', explanation='The Blue Hole is a circular sinkhole that is 300 meters across and 125 meters deep within the Belize Barrier Reef.'),
        
        # Add more authentic geography questions to reach 50+
        QAPair(topic='geography', example='Salar de Uyuni', passage='Salar de Uyuni in Bolivia is the world\'s largest salt flat at 10,582 square kilometers. During the rainy season, it becomes the world\'s largest mirror, perfectly reflecting the sky. The salt flat contains 50-70% of the world\'s lithium reserves. It\'s so flat that NASA uses it to calibrate satellites. The salt is harvested in small pyramids that dot the landscape.', entity='world\'s largest mirror', question='What does Salar de Uyuni become during the rainy season?', answer='world\'s largest mirror', explanation='During the rainy season, Salar de Uyuni becomes the world\'s largest mirror, perfectly reflecting the sky.'),
        
        QAPair(topic='geography', example='Victoria Falls', passage='Victoria Falls on the Zambia-Zimbabwe border is 108 meters high and 1,708 meters wide, making it the largest waterfall in the world by combined height and width. The local name "Mosi-oa-Tunya" means "The Smoke That Thunders." The spray from the falls can be seen from 50 kilometers away. During peak flow, 5 million liters of water fall per minute.', entity='5 million liters per minute', question='How much water flows over Victoria Falls during peak flow?', answer='5 million liters per minute', explanation='During peak flow, 5 million liters of water fall over Victoria Falls per minute.'),
        
        QAPair(topic='geography', example='Antelope Canyon', passage='Antelope Canyon in Arizona is a slot canyon formed by flash flood erosion of Navajo Sandstone. The canyon is only 4 meters wide at its widest point but extends 37 meters deep. Light beams shine down through openings in the canyon, creating spectacular photographic opportunities. The canyon can flood rapidly during rainstorms, making it dangerous to visit without guides.', entity='4 meters wide, 37 meters deep', question='What are the dimensions of Antelope Canyon?', answer='4 meters wide at its widest point, 37 meters deep', explanation='Antelope Canyon is only 4 meters wide at its widest point but extends 37 meters deep.'),
        
        QAPair(topic='geography', example='Socotra Island', passage='Socotra Island off Yemen is so isolated that one-third of its plants exist nowhere else on Earth. The island separated from the Arabian Peninsula 6 million years ago. It\'s home to the Dragon Blood Tree, which looks like an umbrella and bleeds red resin. The island has 700 endemic species and is called the "Galápagos of the Indian Ocean."', entity='one-third plants exist nowhere else', question='What percentage of Socotra Island\'s plants are found nowhere else on Earth?', answer='one-third', explanation='One-third of Socotra Island\'s plants exist nowhere else on Earth due to its 6-million-year isolation.'),
        
        QAPair(topic='geography', example='Chocolate Hills', passage='The Chocolate Hills in the Philippines consist of at least 1,260 hills spread over 50 square kilometers. The hills are nearly symmetrical and turn brown during the dry season, resembling chocolate kisses. They\'re made of limestone covered with grass. Local legend says they were formed by two giants throwing rocks at each other, but they\'re actually ancient coral reefs uplifted by tectonic activity.', entity='1,260 hills over 50 square kilometers', question='How many hills make up the Chocolate Hills and over what area?', answer='at least 1,260 hills over 50 square kilometers', explanation='The Chocolate Hills consist of at least 1,260 hills spread over 50 square kilometers in the Philippines.'),
    ]

if __name__ == "__main__":
    # First, identify formulaic questions
    formulaic_count, authentic_count = identify_and_remove_formulaic_questions()
    
    print(f"\n🔍 Analysis Complete:")
    print(f"  - Formulaic questions found: {formulaic_count}")
    print(f"  - Authentic questions to keep: {authentic_count}")
    print(f"\n⚠️  Need to clear database and rebuild with only authentic questions")
    
    # Create authentic geography questions
    geography_questions = create_authentic_geography_questions()
    print(f"\n✅ Created {len(geography_questions)} authentic geography questions")
    
    print(f"\n📋 Next steps:")
    print(f"  1. Clear database completely")
    print(f"  2. Insert only authentic questions for all topics")
    print(f"  3. Verify no formulaic patterns remain")
