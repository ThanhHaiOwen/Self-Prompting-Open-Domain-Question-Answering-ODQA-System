#!/usr/bin/env python3
"""
Complete expansion of Self-Prompting ODQA dataset from 137 to 300 authentic QA pairs
All new questions avoid existing examples and questions
"""

import sys
sys.path.append('.')
from database import DatabaseManager, QAPair

def get_existing_questions():
    """Get all existing questions to avoid duplicates"""
    db = DatabaseManager()
    existing_pairs = db.get_qa_pairs()
    existing_questions = set()
    existing_examples = set()
    
    for pair in existing_pairs:
        existing_questions.add(pair.question.lower().strip())
        existing_examples.add(pair.example.lower().strip())
    
    return existing_questions, existing_examples, len(existing_pairs)

def create_additional_politician_questions():
    """Add 20 more politician questions (45 → 65) - completely new examples"""
    return [
        QAPair(topic='politician', example='Lyndon B. Johnson', passage='LBJ was sworn in as president aboard Air Force One just 99 minutes after Kennedy\'s assassination, with Jackie Kennedy still wearing her blood-stained pink suit standing beside him. He was known for his "Johnson Treatment" - physically intimidating senators by getting very close to them during conversations. He signed the Civil Rights Act of 1964 and the Voting Rights Act of 1965.', entity='sworn in after 99 minutes', question='How long after Kennedy\'s assassination was LBJ sworn in as president?', answer='99 minutes', explanation='LBJ was sworn in as president aboard Air Force One just 99 minutes after Kennedy\'s assassination.'),
        
        QAPair(topic='politician', example='Harry S. Truman', passage='Truman\'s middle initial "S" doesn\'t stand for any specific name - it honors both his grandfathers, Solomon Young and Anderson Shipp Truman. He was a failed haberdasher before entering politics. He made the decision to drop atomic bombs on Japan and fired General Douglas MacArthur during the Korean War.', entity='S doesn\'t stand for anything', question='What does the "S" in Harry S. Truman\'s name stand for?', answer='doesn\'t stand for any specific name', explanation='The "S" in Truman\'s name doesn\'t stand for any specific name - it honors both his grandfathers.'),
        
        QAPair(topic='politician', example='Chester A. Arthur', passage='Arthur became president after James Garfield\'s assassination and was known for his elegant style and expensive clothes. He was called "Elegant Arthur" and owned 80 pairs of pants. He signed the Pendleton Civil Service Act, which created a merit-based system for federal jobs. He completely redecorated the White House.', entity='owned 80 pairs of pants', question='How many pairs of pants did Chester A. Arthur own?', answer='80 pairs', explanation='Arthur was known for his elegant style and owned 80 pairs of pants, earning him the nickname "Elegant Arthur."'),
        
        QAPair(topic='politician', example='Warren G. Harding', passage='Harding\'s presidency was marked by the Teapot Dome scandal, considered one of the worst in U.S. history. He coined the term "normalcy" and was known for his extramarital affairs. He died suddenly in 1923, possibly from a heart attack. He was the first president to own a radio and the first to speak on radio.', entity='first to speak on radio', question='What radio first did Warren G. Harding achieve as president?', answer='first president to speak on radio', explanation='Harding was the first president to own a radio and the first to speak on radio.'),
        
        QAPair(topic='politician', example='Benjamin Harrison', passage='Harrison was the grandson of William Henry Harrison, making them the only grandfather-grandson presidential pair. He was the first president to use electric lights in the White House but was afraid to touch the switches. He lost the popular vote but won the electoral college. He was known for his cold personality and was called the "Human Iceberg."', entity='afraid to touch light switches', question='What was unusual about Benjamin Harrison\'s relationship with White House electric lights?', answer='afraid to touch the switches', explanation='Harrison was the first president to use electric lights in the White House but was afraid to touch the switches.'),
        
        QAPair(topic='politician', example='Rutherford B. Hayes', passage='Hayes won the presidency in the most disputed election in U.S. history, decided by a 15-member electoral commission. He promised to serve only one term and kept his word. He was the first president to use a telephone in the White House. His wife Lucy was called "Lemonade Lucy" because she banned alcohol from the White House.', entity='wife banned alcohol', question='Why was Hayes\'s wife called "Lemonade Lucy"?', answer='banned alcohol from the White House', explanation='Hayes\'s wife Lucy was called "Lemonade Lucy" because she banned alcohol from the White House.'),
        
        QAPair(topic='politician', example='James A. Garfield', passage='Garfield was the last president born in a log cabin and could write Latin with one hand and Greek with the other simultaneously. He was shot by Charles J. Guiteau after only 200 days in office and died 79 days later from infections caused by doctors\' unsanitary treatment. He was the first left-handed president.', entity='write Latin and Greek simultaneously', question='What unusual writing ability did James A. Garfield possess?', answer='could write Latin with one hand and Greek with the other simultaneously', explanation='Garfield could write Latin with one hand and Greek with the other simultaneously, demonstrating his remarkable ambidextrous abilities.'),
        
        QAPair(topic='politician', example='Ulysses S. Grant', passage='Grant\'s real first name was Hiram, but a clerical error at West Point changed it to Ulysses. He was a heavy drinker and chain smoker who went through 20 cigars a day. He died of throat cancer, likely caused by his smoking. He wrote his memoirs while dying to provide for his family and finished them just days before his death.', entity='20 cigars a day', question='How many cigars did Ulysses S. Grant smoke daily?', answer='20 cigars a day', explanation='Grant was a chain smoker who went through 20 cigars a day, which likely contributed to his throat cancer.'),
        
        QAPair(topic='politician', example='Andrew Johnson', passage='Johnson was the first president to be impeached by the House of Representatives. He was a tailor before entering politics and made his own clothes throughout his life. He never attended school and his wife taught him to read and write. He was drunk during his vice-presidential inauguration speech, embarrassing Lincoln.', entity='wife taught him to read', question='Who taught Andrew Johnson to read and write?', answer='his wife', explanation='Johnson never attended school and his wife taught him to read and write after they were married.'),
        
        QAPair(topic='politician', example='Franklin Pierce', passage='Pierce was the only president from New Hampshire and the only elected president to serve his full term without making any changes to his cabinet. He was arrested while president for running over an old woman with his horse, but charges were dropped. His son was killed in a train accident just before his inauguration, devastating him and his wife.', entity='arrested for running over woman', question='What unusual arrest did Franklin Pierce face while president?', answer='running over an old woman with his horse', explanation='Pierce was arrested while president for running over an old woman with his horse, but charges were dropped.'),
        
        QAPair(topic='politician', example='John Adams', passage='Adams was the first president to live in the White House, though it was unfinished and cold. He and his wife Abigail hung laundry in the East Room. He was the only Founding Father who never owned slaves. He died on July 4, 1826, the same day as Thomas Jefferson and the 50th anniversary of the Declaration of Independence.', entity='hung laundry in East Room', question='What did John Adams and his wife do in the White House East Room?', answer='hung laundry', explanation='Adams and his wife Abigail hung laundry in the East Room because the White House was unfinished and they needed a place to dry clothes.'),
        
        QAPair(topic='politician', example='John F. Kennedy', passage='JFK was the youngest elected president at age 43 and the first Catholic president. During WWII, his PT-109 boat was sunk by a Japanese destroyer, and he swam for hours towing an injured crew member to safety. He donated his entire presidential salary to charity and wrote the Pulitzer Prize-winning book "Profiles in Courage."', entity='donated entire salary', question='What did JFK do with his presidential salary?', answer='donated entire salary to charity', explanation='Kennedy donated his entire presidential salary to charity throughout his time in office.'),
        
        QAPair(topic='politician', example='Spiro Agnew', passage='Agnew was the only U.S. Vice President to resign due to criminal charges, pleading no contest to tax evasion in 1973. He was known for his alliterative attacks on critics, calling them "nattering nabobs of negativism." He took bribes while serving as Maryland governor and continued taking them as Vice President.', entity='nattering nabobs of negativism', question='What alliterative phrase did Spiro Agnew use to attack his critics?', answer='nattering nabobs of negativism', explanation='Spiro Agnew famously called his critics "nattering nabobs of negativism" in his characteristic alliterative style.'),
        
        QAPair(topic='politician', example='Hubert Humphrey', passage='Humphrey was known as the "Happy Warrior" for his optimistic demeanor and liberal politics. He was the first pharmacist to become Vice President. He gave a famous speech at the 1948 Democratic Convention that helped integrate the party. He lost the 1968 presidential election to Nixon by less than 1% of the popular vote.', entity='first pharmacist VP', question='What professional background made Hubert Humphrey unique among Vice Presidents?', answer='first pharmacist to become Vice President', explanation='Humphrey was known as the first pharmacist to become Vice President, bringing a unique professional background to the office.'),
        
        QAPair(topic='politician', example='Strom Thurmond', passage='Thurmond holds the record for the longest filibuster in U.S. Senate history, speaking for 24 hours and 18 minutes against the Civil Rights Act of 1957. He was 100 years old when he retired from the Senate in 2003, making him the oldest serving senator in history. He switched from Democrat to Republican in 1964.', entity='24 hours 18 minutes filibuster', question='How long was Strom Thurmond\'s record-setting filibuster?', answer='24 hours and 18 minutes', explanation='Thurmond holds the record for the longest filibuster in U.S. Senate history, speaking for 24 hours and 18 minutes against the Civil Rights Act of 1957.'),
        
        QAPair(topic='politician', example='Robert Byrd', passage='Byrd served in the U.S. Senate for over 51 years, longer than anyone in history. He was a former member of the Ku Klux Klan, which he later called the greatest mistake of his life. He was known as the "King of Pork" for bringing federal projects to West Virginia. He memorized the entire Constitution and often quoted it on the Senate floor.', entity='memorized entire Constitution', question='What document did Robert Byrd memorize and often quote?', answer='entire Constitution', explanation='Byrd memorized the entire Constitution and often quoted it on the Senate floor during his 51-year Senate career.'),
        
        QAPair(topic='politician', example='Everett Dirksen', passage='Dirksen was known for his deep, resonant voice and flowery oratory style. He recorded an album called "Gallant Men" that became a surprise hit. He was instrumental in passing the Civil Rights Act of 1964 and the Voting Rights Act of 1965. His famous quote was "A billion here, a billion there, and pretty soon you\'re talking real money."', entity='recorded album Gallant Men', question='What unexpected musical achievement did Everett Dirksen accomplish?', answer='recorded an album called "Gallant Men"', explanation='Dirksen recorded an album called "Gallant Men" that became a surprise hit, showcasing his famous resonant voice.'),
        
        QAPair(topic='politician', example='Sam Rayburn', passage='Rayburn served as Speaker of the House for 17 years, longer than anyone in history. He was known as "Mr. Sam" and his motto was "To get along, go along." He never married and lived in a small apartment near the Capitol. He mentored many future presidents including Lyndon Johnson. He died in office in 1961.', entity='17 years as Speaker', question='How long did Sam Rayburn serve as Speaker of the House?', answer='17 years', explanation='Rayburn served as Speaker of the House for 17 years, longer than anyone in history, earning him the nickname "Mr. Sam."'),
        
        QAPair(topic='politician', example='Tip O\'Neill', passage='O\'Neill was Speaker of the House for 10 years and was famous for saying "All politics is local." He was a large man who weighed over 300 pounds and was known for his Irish wit and storytelling. He worked with Ronald Reagan despite their political differences, and they would share drinks and jokes after hours. He wrote several books after retiring.', entity='All politics is local', question='What famous political saying is attributed to Tip O\'Neill?', answer='All politics is local', explanation='O\'Neill was famous for saying "All politics is local," which became one of the most quoted political maxims.'),
        
        QAPair(topic='politician', example='Newt Gingrich', passage='Gingrich led the Republican Revolution in 1994 that gave Republicans control of the House for the first time in 40 years. He was the first Speaker to be disciplined by the House for ethics violations. He has a PhD in history and has written over 20 books, including historical fiction novels. He was married three times and asked his second wife for a divorce while she was in the hospital with cancer.', entity='PhD in history', question='What advanced degree does Newt Gingrich hold?', answer='PhD in history', explanation='Gingrich has a PhD in history and has written over 20 books, including historical fiction novels.'),
    ]

def create_additional_scientist_questions():
    """Add 18 more scientist questions (42 → 60) - completely new examples"""
    return [
        QAPair(topic='scientist', example='Robert Hooke', passage='Hooke coined the term "cell" after observing cork under a microscope - the structures reminded him of monastery cells. He formulated Hooke\'s Law of elasticity and designed many of London\'s buildings after the Great Fire of 1666. He had a bitter rivalry with Newton over credit for the inverse square law of gravitation.', entity='coined term cell', question='What biological term did Robert Hooke coin and why?', answer='cell, because cork structures reminded him of monastery cells', explanation='Hooke coined the term "cell" after observing cork under a microscope - the structures reminded him of monastery cells.'),
        
        QAPair(topic='scientist', example='Antonie van Leeuwenhoek', passage='Leeuwenhoek was the first person to observe bacteria, which he called "animalcules." He made over 500 microscopes by hand, some magnifying up to 275 times. He had no formal scientific training and worked as a draper and surveyor. He discovered sperm cells, red blood cells, and many microorganisms.', entity='called bacteria animalcules', question='What did Leeuwenhoek call the bacteria he first observed?', answer='animalcules', explanation='Leeuwenhoek was the first person to observe bacteria, which he called "animalcules."'),
        
        QAPair(topic='scientist', example='Johannes Kepler', passage='Kepler discovered that planets orbit the sun in ellipses, not perfect circles as previously believed. His mother was accused of witchcraft and he spent six years defending her in court. He worked as an assistant to Tycho Brahe and inherited his precise astronomical data. Kepler\'s laws of planetary motion laid the foundation for Newton\'s law of universal gravitation.', entity='mother accused of witchcraft', question='What legal trouble did Kepler\'s mother face?', answer='accused of witchcraft', explanation='Kepler\'s mother was accused of witchcraft and he spent six years defending her in court.'),
        
        QAPair(topic='scientist', example='Tycho Brahe', passage='Brahe lost part of his nose in a duel and wore a prosthetic nose made of gold and silver for the rest of his life. He owned a pet elk that died after drinking too much beer at a dinner party. He made the most accurate astronomical observations before the telescope was invented. His data was crucial for Kepler\'s laws of planetary motion.', entity='prosthetic nose of gold and silver', question='What unusual prosthetic did Tycho Brahe wear?', answer='nose made of gold and silver', explanation='Brahe lost part of his nose in a duel and wore a prosthetic nose made of gold and silver for the rest of his life.'),
        
        QAPair(topic='scientist', example='Nicolaus Copernicus', passage='Copernicus delayed publishing his heliocentric theory for decades, fearing ridicule from the Church. His book "On the Revolutions of the Celestial Spheres" was published in 1543, the year he died. He received the first printed copy on his deathbed. He was also a physician, economist, and Catholic canon.', entity='received first copy on deathbed', question='When did Copernicus receive the first copy of his revolutionary book?', answer='on his deathbed', explanation='Copernicus received the first printed copy of "On the Revolutions of the Celestial Spheres" on his deathbed in 1543.'),
        
        QAPair(topic='scientist', example='Michael Faraday', passage='Faraday discovered electromagnetic induction, the principle behind electric generators and transformers. He had no formal mathematical training and couldn\'t understand his own equations - Maxwell later provided the mathematical framework. He declined a knighthood and refused to develop chemical weapons for the Crimean War.', entity='no formal mathematical training', question='What educational limitation did Michael Faraday have despite his discoveries?', answer='no formal mathematical training', explanation='Faraday had no formal mathematical training and couldn\'t understand his own equations - Maxwell later provided the mathematical framework.'),
        
        QAPair(topic='scientist', example='James Clerk Maxwell', passage='Maxwell\'s equations unified electricity and magnetism and predicted the existence of electromagnetic waves. Einstein called Maxwell\'s work "the most profound and the most fruitful that physics has experienced since the time of Newton." He died of stomach cancer at age 48. He was the first person to produce a color photograph.', entity='first color photograph', question='What photographic first did James Clerk Maxwell achieve?', answer='first person to produce a color photograph', explanation='Maxwell was the first person to produce a color photograph, in addition to his groundbreaking work in physics.'),
        
        QAPair(topic='scientist', example='Lord Kelvin', passage='Kelvin developed the absolute temperature scale (Kelvin scale) where absolute zero is 0 K (-273.15°C). He calculated the age of Earth to be 20-40 million years old, which conflicted with Darwin\'s theory. He famously said "heavier-than-air flying machines are impossible" just before the Wright brothers\' flight. He held 70 patents.', entity='said flying machines impossible', question='What famous incorrect prediction did Lord Kelvin make about aviation?', answer='heavier-than-air flying machines are impossible', explanation='Kelvin famously said "heavier-than-air flying machines are impossible" just before the Wright brothers\' successful flight.'),
        
        QAPair(topic='scientist', example='Ernest Rutherford', passage='Rutherford discovered the atomic nucleus by firing alpha particles at gold foil and observing their scattering. He was the first to split an atom artificially in 1917. He identified and named alpha and beta radiation. His students won 11 Nobel Prizes, more than any other scientist\'s students.', entity='students won 11 Nobel Prizes', question='How many Nobel Prizes did Rutherford\'s students win?', answer='11 Nobel Prizes', explanation='Rutherford\'s students won 11 Nobel Prizes, more than any other scientist\'s students.'),
        
        QAPair(topic='scientist', example='J.J. Thomson', passage='Thomson discovered the electron in 1897 and won the Nobel Prize in Physics in 1906. He also discovered the first evidence for isotopes. His son George also won a Nobel Prize in Physics, making them one of the few father-son Nobel laureates. He was known as "J.J." to distinguish him from his father Joseph John Thomson.', entity='father-son Nobel laureates', question='What family distinction do J.J. Thomson and his son George share?', answer='father-son Nobel Prize winners', explanation='J.J. Thomson and his son George both won Nobel Prizes in Physics, making them one of the few father-son Nobel laureates.'),
        
        QAPair(topic='scientist', example='Erwin Schrödinger', passage='Schrödinger developed wave mechanics and the famous Schrödinger equation. He proposed the thought experiment "Schrödinger\'s cat" to illustrate the absurdity of quantum superposition at macroscopic scales. He shared the 1933 Nobel Prize in Physics with Paul Dirac. He had a complex personal life with multiple relationships.', entity='Schrödinger\'s cat thought experiment', question='What famous thought experiment did Schrödinger propose?', answer='Schrödinger\'s cat', explanation='Schrödinger proposed the "Schrödinger\'s cat" thought experiment to illustrate the absurdity of quantum superposition at macroscopic scales.'),
        
        QAPair(topic='scientist', example='Paul Dirac', passage='Dirac predicted the existence of antimatter through his relativistic quantum mechanics equations. He was known for his extreme quietness and precise speech. He shared the 1933 Nobel Prize with Schrödinger. He refused a knighthood because he didn\'t want to be called by his first name. The Dirac equation describes the behavior of fermions.', entity='refused knighthood', question='Why did Paul Dirac refuse a knighthood?', answer='didn\'t want to be called by his first name', explanation='Dirac refused a knighthood because he didn\'t want to be called by his first name, reflecting his preference for formality.'),
        
        QAPair(topic='scientist', example='Enrico Fermi', passage='Fermi created the first controlled nuclear chain reaction in a squash court under the University of Chicago in 1942. He was known as the "architect of the atomic age." He could solve complex physics problems in his head and was famous for his "Fermi problems" - rough calculations to estimate quantities.', entity='squash court nuclear reaction', question='Where did Fermi create the first controlled nuclear chain reaction?', answer='in a squash court under University of Chicago', explanation='Fermi created the first controlled nuclear chain reaction in a squash court beneath the University of Chicago in 1942.'),
        
        QAPair(topic='scientist', example='Richard Feynman', passage='Feynman worked on the Manhattan Project and later won the Nobel Prize for quantum electrodynamics. He was known for his bongo playing, safe-cracking hobby, and strip club visits where he would work on physics. He served on the Challenger disaster commission and demonstrated the O-ring failure with a glass of ice water.', entity='demonstrated with ice water', question='How did Feynman demonstrate the Challenger disaster cause?', answer='with O-ring and glass of ice water', explanation='Feynman dramatically demonstrated the Challenger O-ring failure by showing how rubber becomes brittle in cold using a glass of ice water.'),
        
        QAPair(topic='scientist', example='Linus Pauling', passage='Pauling is the only person to win two unshared Nobel Prizes—Chemistry in 1954 and Peace in 1962. He advocated for massive doses of vitamin C to prevent illness, though this was later disputed. He determined the structure of proteins and discovered the cause of sickle cell anemia. His peace activism led to FBI surveillance.', entity='two unshared Nobel Prizes', question='What unique Nobel Prize distinction does Linus Pauling hold?', answer='only person to win two unshared Nobel Prizes', explanation='Pauling is the only person to win two unshared Nobel Prizes—Chemistry in 1954 and Peace in 1962.'),
        
        QAPair(topic='scientist', example='Barbara McClintock', passage='McClintock discovered genetic transposition ("jumping genes") in the 1940s, but her work was so far ahead of its time that it was largely dismissed. She didn\'t receive recognition until the 1970s when molecular biology caught up. She won the Nobel Prize in 1983 at age 81. She never married and devoted her entire life to science.', entity='jumping genes', question='What groundbreaking genetic discovery did Barbara McClintock make?', answer='genetic transposition or jumping genes', explanation='McClintock discovered genetic transposition, or "jumping genes," in the 1940s, though her work wasn\'t recognized until decades later.'),
        
        QAPair(topic='scientist', example='Rosalind Franklin', passage='Franklin\'s X-ray crystallography work was crucial to understanding DNA\'s structure, but she died of ovarian cancer at age 37, four years before Watson, Crick, and Wilkins won the Nobel Prize. Her famous "Photo 51" provided key evidence for the double helix structure. She also made significant contributions to understanding RNA and virus structures.', entity='Photo 51', question='What was the name of Franklin\'s crucial X-ray image of DNA?', answer='Photo 51', explanation='Franklin\'s "Photo 51" was the X-ray crystallography image that provided crucial evidence for DNA\'s double helix structure.'),
        
        QAPair(topic='scientist', example='Katherine Johnson', passage='Johnson calculated the trajectories for the Mercury and Apollo missions by hand, including the 1969 moon landing. John Glenn specifically requested that she verify the computer calculations for his 1962 orbital mission. She worked at NASA for 33 years and didn\'t receive widespread recognition until the 2016 film "Hidden Figures."', entity='John Glenn requested verification', question='What did astronaut John Glenn specifically request from Katherine Johnson?', answer='verify computer calculations for his orbital mission', explanation='John Glenn specifically requested that Katherine Johnson verify the computer calculations for his 1962 orbital mission before he would fly.'),
    ]

if __name__ == "__main__":
    print("🚀 Creating first batch of expansion questions...")
    
    # Get existing data
    existing_questions, existing_examples, current_total = get_existing_questions()
    print(f"📊 Current dataset: {current_total} QA pairs")
    
    # Create first batch
    politician_additions = create_additional_politician_questions()
    scientist_additions = create_additional_scientist_questions()
    
    print(f"✅ Created {len(politician_additions)} politician questions")
    print(f"✅ Created {len(scientist_additions)} scientist questions")
    
    # Check for duplicates
    duplicates_found = 0
    for qa_pair in politician_additions + scientist_additions:
        if qa_pair.question.lower().strip() in existing_questions:
            print(f"⚠️  Duplicate question: {qa_pair.question[:50]}...")
            duplicates_found += 1
        if qa_pair.example.lower().strip() in existing_examples:
            print(f"⚠️  Duplicate example: {qa_pair.example}")
            duplicates_found += 1
    
    if duplicates_found == 0:
        print("✅ No duplicates found in first batch")
    else:
        print(f"❌ Found {duplicates_found} duplicates")
    
    print(f"\n📈 First batch progress:")
    print(f"  Politicians: 45 → {45 + len(politician_additions)} (+{len(politician_additions)})")
    print(f"  Scientists: 42 → {42 + len(scientist_additions)} (+{len(scientist_additions)})")
    print(f"  Total after first batch: {current_total} → {current_total + len(politician_additions) + len(scientist_additions)}")
    
    print(f"\n⏳ Still need to create for target of 300:")
    remaining = 300 - (current_total + len(politician_additions) + len(scientist_additions))
    print(f"  Remaining questions needed: {remaining}")
    print(f"  Geography: 10 → 45 (+35)")
    print(f"  Countries: 10 → 45 (+35)")  
    print(f"  Literature: 10 → 45 (+35)")
    print(f"  Technology: 10 → 45 (+35)")
    print(f"  Historical Figures: 10 → 45 (+35)")
