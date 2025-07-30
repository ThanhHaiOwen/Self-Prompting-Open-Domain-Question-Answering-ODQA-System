#!/usr/bin/env python3
"""
Expand Self-Prompting ODQA dataset from 137 to ~300 authentic QA pairs
Target distribution:
- Politicians: 45 → 65 (+20)
- Scientists: 42 → 60 (+18) 
- Geography: 10 → 45 (+35)
- Countries: 10 → 45 (+35)
- Literature: 10 → 45 (+35)
- Technology: 10 → 45 (+35)
- Historical Figures: 10 → 45 (+35)
Total: 137 → 300 (+163)
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
    
    return existing_questions, existing_examples

def create_additional_politician_questions():
    """Add 20 more politician questions (45 → 65) - avoiding existing examples"""
    return [
        QAPair(topic='politician', example='Lyndon B. Johnson', passage='LBJ was sworn in as president aboard Air Force One just 99 minutes after Kennedy\'s assassination, with Jackie Kennedy still wearing her blood-stained pink suit standing beside him. He was known for his "Johnson Treatment" - physically intimidating senators by getting very close to them during conversations. He signed the Civil Rights Act of 1964 and the Voting Rights Act of 1965. He chose not to run for re-election in 1968 due to the Vietnam War.', entity='sworn in after 99 minutes', question='How long after Kennedy\'s assassination was LBJ sworn in as president?', answer='99 minutes', explanation='LBJ was sworn in as president aboard Air Force One just 99 minutes after Kennedy\'s assassination.'),

        QAPair(topic='politician', example='Harry S. Truman', passage='Truman\'s middle initial "S" doesn\'t stand for any specific name - it honors both his grandfathers, Solomon Young and Anderson Shipp Truman. He was a failed haberdasher before entering politics. He made the decision to drop atomic bombs on Japan and fired General Douglas MacArthur during the Korean War. His approval rating dropped to 22% in 1952, one of the lowest in presidential history.', entity='S doesn\'t stand for anything', question='What does the "S" in Harry S. Truman\'s name stand for?', answer='doesn\'t stand for any specific name', explanation='The "S" in Truman\'s name doesn\'t stand for any specific name - it honors both his grandfathers, Solomon Young and Anderson Shipp Truman.'),

        QAPair(topic='politician', example='Ronald Reagan', passage='Reagan was a Hollywood actor who appeared in over 50 films before entering politics. He was shot by John Hinckley Jr. on March 30, 1981, just 69 days into his presidency. He told his wife Nancy "Honey, I forgot to duck" after the shooting. He was the oldest president when elected at age 69. He was known as "The Great Communicator" and helped end the Cold War.', entity='shot after 69 days', question='How many days into Reagan\'s presidency was he shot?', answer='69 days', explanation='Reagan was shot by John Hinckley Jr. on March 30, 1981, just 69 days into his presidency.'),

        QAPair(topic='politician', example='Dwight D. Eisenhower', passage='Eisenhower was Supreme Allied Commander in Europe during WWII and planned D-Day. He never held elected office before becoming president. He created the Interstate Highway System, which was inspired by German autobahns he saw during the war. He warned about the "military-industrial complex" in his farewell address. He was the first president to appear on color television.', entity='first on color TV', question='What television first did Eisenhower achieve as president?', answer='first president to appear on color television', explanation='Eisenhower was the first president to appear on color television.'),

        QAPair(topic='politician', example='Gerald Ford', passage='Ford is the only person to serve as both Vice President and President without being elected to either office. He became VP when Spiro Agnew resigned, then President when Nixon resigned. He pardoned Nixon for any crimes he may have committed as president. He survived two assassination attempts in September 1975, both by women. He was a star football player at the University of Michigan.', entity='two assassination attempts by women', question='What unusual characteristic marked the assassination attempts on Gerald Ford?', answer='both attempts were by women', explanation='Ford survived two assassination attempts in September 1975, both by women, which was unusual in presidential history.'),

        QAPair(topic='politician', example='Jimmy Carter', passage='Carter was a peanut farmer from Georgia who taught Sunday school. He carried his own luggage and sold the presidential yacht to save money. He was attacked by a swimming rabbit while fishing, leading to the "killer rabbit" incident. He won the Nobel Peace Prize in 2002 for his humanitarian work. He built homes for Habitat for Humanity well into his 90s.', entity='attacked by swimming rabbit', question='What unusual animal encounter did Jimmy Carter have while president?', answer='attacked by a swimming rabbit', explanation='Carter was attacked by a swimming rabbit while fishing, leading to the famous "killer rabbit" incident.'),

        QAPair(topic='politician', example='Woodrow Wilson', passage='Wilson was the only president to hold a PhD (in political science from Johns Hopkins). He suffered a severe stroke in 1919 that left him partially paralyzed, and his wife Edith effectively ran the country for the remainder of his term. He established the Federal Reserve System and led the U.S. into World War I. He won the Nobel Peace Prize for his work on the League of Nations.', entity='only president with PhD', question='What educational distinction does Woodrow Wilson hold among presidents?', answer='only president to hold a PhD', explanation='Wilson was the only president to hold a PhD, which he earned in political science from Johns Hopkins University.'),

        QAPair(topic='politician', example='Calvin Coolidge', passage='Coolidge was known as "Silent Cal" because he spoke very little. When a dinner guest bet she could get him to say more than two words, he replied "You lose." He was sworn in by his father, a notary public, by kerosene lamp at 2:47 AM after Harding\'s death. He believed "the business of America is business" and presided over the Roaring Twenties economic boom.', entity='sworn in by father at 2:47 AM', question='Who swore in Calvin Coolidge as president and at what time?', answer='his father at 2:47 AM', explanation='Coolidge was sworn in by his father, a notary public, by kerosene lamp at 2:47 AM after Harding\'s death.'),

        QAPair(topic='politician', example='Herbert Hoover', passage='Hoover was a successful mining engineer who became a millionaire before age 40. He organized food relief for Belgium during WWI and was called "The Great Humanitarian." He was president during the start of the Great Depression and was blamed for it, leading to shantytowns being called "Hoovervilles." He lived longer after leaving office than any other president - 31 years.', entity='lived 31 years after office', question='How long did Herbert Hoover live after leaving the presidency?', answer='31 years', explanation='Hoover lived longer after leaving office than any other president - 31 years.'),

        QAPair(topic='politician', example='William Howard Taft', passage='Taft is the only person to serve as both President and Chief Justice of the Supreme Court. He weighed over 300 pounds and once got stuck in the White House bathtub, requiring a new larger tub to be installed. He was more interested in being a judge than president and was happier on the Supreme Court. He established the federal income tax through the 16th Amendment.', entity='got stuck in bathtub', question='What embarrassing incident happened to Taft in the White House?', answer='got stuck in the bathtub', explanation='Taft weighed over 300 pounds and once got stuck in the White House bathtub, requiring a new larger tub to be installed.'),

        QAPair(topic='politician', example='Grover Cleveland', passage='Cleveland is the only president to serve non-consecutive terms (22nd and 24th president). He was a bachelor when elected and married Frances Folsom in the White House - she was 21 and he was 49. He was known as "Grover the Good" for his honesty. He underwent secret surgery for mouth cancer aboard a yacht to avoid public panic during an economic crisis.', entity='secret surgery on yacht', question='Where did Grover Cleveland undergo secret cancer surgery?', answer='aboard a yacht', explanation='Cleveland underwent secret surgery for mouth cancer aboard a yacht to avoid public panic during an economic crisis.'),

        QAPair(topic='politician', example='Millard Fillmore', passage='Fillmore was the last Whig president and installed the first bathtub and kitchen stove in the White House. He was never elected president - he became president when Zachary Taylor died. He sent Commodore Perry to open trade with Japan. After his presidency, he was nominated by the Know-Nothing Party in 1856. He founded the University at Buffalo.', entity='installed first bathtub', question='What White House first did Millard Fillmore install?', answer='first bathtub and kitchen stove', explanation='Fillmore installed the first bathtub and kitchen stove in the White House.'),

        QAPair(topic='politician', example='Zachary Taylor', passage='Taylor was a career military officer who never voted in a presidential election before becoming president himself. He owned a plantation with over 100 slaves but opposed the expansion of slavery. He died after 16 months in office, possibly from gastroenteritis after consuming large quantities of cold milk and cherries on July 4th. His body was exhumed in 1991 to test for arsenic poisoning, but none was found.', entity='never voted before becoming president', question='What unusual voting record did Zachary Taylor have before becoming president?', answer='never voted in a presidential election', explanation='Taylor was a career military officer who never voted in a presidential election before becoming president himself.'),

        QAPair(topic='politician', example='James K. Polk', passage='Polk promised to serve only one term and kept his word. He achieved all four of his campaign goals: lowering tariffs, establishing an independent treasury, settling the Oregon boundary, and acquiring California. He expanded the U.S. by about one-third through the Mexican-American War. He worked so hard that he died just 103 days after leaving office, making his post-presidency the shortest in history.', entity='died 103 days after office', question='How long did James K. Polk live after leaving the presidency?', answer='103 days', explanation='Polk worked so hard that he died just 103 days after leaving office, making his post-presidency the shortest in history.'),

        QAPair(topic='politician', example='John Tyler', passage='Tyler was expelled from his own Whig Party while serving as president, earning him the nickname "His Accidency." He had 15 children with two wives - more than any other president. His 10th child was born when he was 63. He later served in the Confederate Congress during the Civil War. He died in 1862 and was the only president whose death was not officially mourned by the U.S. government.', entity='15 children', question='How many children did John Tyler have?', answer='15 children', explanation='Tyler had 15 children with two wives - more than any other president.'),

        QAPair(topic='politician', example='Martin Van Buren', passage='Van Buren was the first president born as a U.S. citizen (previous presidents were born as British subjects). He was known as "Old Kinderhook" and his supporters were called "O.K.," which may be the origin of the term "okay." He spoke Dutch as his first language. He served as Andrew Jackson\'s Vice President and was hand-picked as his successor.', entity='first born as U.S. citizen', question='What citizenship distinction does Martin Van Buren hold among presidents?', answer='first president born as a U.S. citizen', explanation='Van Buren was the first president born as a U.S. citizen, as previous presidents were born as British subjects.'),

        QAPair(topic='politician', example='William Henry Harrison', passage='Harrison gave the longest inaugural address in history - 8,445 words lasting nearly two hours in cold, wet weather without a coat or hat. He died of pneumonia 31 days later, making his the shortest presidency. He was 68 when inaugurated, making him the oldest president until Reagan. His grandson Benjamin Harrison also became president. He was the last president born as a British subject.', entity='8,445 words inaugural address', question='How long was William Henry Harrison\'s inaugural address?', answer='8,445 words', explanation='Harrison gave the longest inaugural address in history - 8,445 words lasting nearly two hours in cold, wet weather.'),

        QAPair(topic='politician', example='James Madison', passage='Madison was the shortest president at 5 feet 4 inches and weighed about 100 pounds. He was called the "Father of the Constitution" for his role in drafting it. He was the first president to wear long pants instead of knee breeches. During the War of 1812, he became the only president to lead troops in battle while in office. His wife Dolley saved George Washington\'s portrait when the British burned the White House.', entity='shortest at 5 feet 4 inches', question='What physical distinction does James Madison hold among presidents?', answer='shortest president at 5 feet 4 inches', explanation='Madison was the shortest president at 5 feet 4 inches and weighed about 100 pounds.'),

        QAPair(topic='politician', example='James Monroe', passage='Monroe was the last president who was a Founding Father and the last to wear a powdered wig. His presidency was called the "Era of Good Feelings" because there was little partisan conflict. He established the Monroe Doctrine, warning European powers not to interfere in the Americas. He died on July 4, 1831, making him the third president to die on Independence Day.', entity='third to die on July 4', question='What Independence Day distinction does James Monroe share with other presidents?', answer='third president to die on July 4', explanation='Monroe died on July 4, 1831, making him the third president to die on Independence Day, after Adams and Jefferson.'),

        # Replace John Quincy Adams with a different politician to avoid duplicate
        QAPair(topic='politician', example='Chester A. Arthur', passage='Arthur became president after James Garfield\'s assassination and was known for his elegant style and expensive clothes. He was called "Elegant Arthur" and owned 80 pairs of pants. He signed the Pendleton Civil Service Act, which created a merit-based system for federal jobs. He was a collector of fine wines and completely redecorated the White House. He destroyed most of his papers before his death.', entity='owned 80 pairs of pants', question='How many pairs of pants did Chester A. Arthur own?', answer='80 pairs', explanation='Arthur was known for his elegant style and owned 80 pairs of pants, earning him the nickname "Elegant Arthur."'),
    ]

def create_additional_scientist_questions():
    """Add 18 more scientist questions (42 → 60)"""
    return [
        QAPair(topic='scientist', example='Galileo Galilei', passage='Galileo was tried by the Inquisition for supporting heliocentrism and spent his last years under house arrest. He improved the telescope and discovered four moons of Jupiter, now called the Galilean moons. He allegedly said "And yet it moves" after being forced to recant his support for the heliocentric model. The Catholic Church didn\'t officially pardon him until 1992, 350 years after his trial.', entity='pardoned in 1992', question='When did the Catholic Church officially pardon Galileo?', answer='1992', explanation='The Catholic Church didn\'t officially pardon Galileo for his support of heliocentrism until 1992, over 350 years after his trial.'),
        
        QAPair(topic='scientist', example='Johannes Kepler', passage='Kepler discovered that planets orbit the sun in ellipses, not perfect circles as previously believed. His mother was accused of witchcraft and he spent six years defending her in court. He worked as an assistant to Tycho Brahe and inherited his precise astronomical data. Kepler\'s laws of planetary motion laid the foundation for Newton\'s law of universal gravitation.', entity='mother accused of witchcraft', question='What legal trouble did Kepler\'s mother face?', answer='accused of witchcraft', explanation='Kepler\'s mother was accused of witchcraft and he spent six years defending her in court.'),
        
        QAPair(topic='scientist', example='Copernicus', passage='Copernicus delayed publishing his heliocentric theory for decades, fearing ridicule from the Church and fellow scholars. His book "On the Revolutions of the Celestial Spheres" was published in 1543, the year he died. He received the first printed copy on his deathbed. He was also a physician, economist, and Catholic canon. His theory wasn\'t widely accepted until Galileo\'s observations confirmed it.', entity='received first copy on deathbed', question='When did Copernicus receive the first copy of his revolutionary book?', answer='on his deathbed', explanation='Copernicus received the first printed copy of "On the Revolutions of the Celestial Spheres" on his deathbed in 1543.'),
        
        QAPair(topic='scientist', example='Robert Hooke', passage='Hooke coined the term "cell" after observing cork under a microscope - the structures reminded him of monastery cells. He formulated Hooke\'s Law of elasticity and designed many of London\'s buildings after the Great Fire of 1666. He had a bitter rivalry with Newton over credit for the inverse square law of gravitation. He was also an accomplished architect and surveyor.', entity='coined term cell', question='What biological term did Robert Hooke coin and why?', answer='cell, because cork structures reminded him of monastery cells', explanation='Hooke coined the term "cell" after observing cork under a microscope - the structures reminded him of monastery cells.'),
        
        QAPair(topic='scientist', example='Antonie van Leeuwenhoek', passage='Leeuwenhoek was the first person to observe bacteria, which he called "animalcules." He made over 500 microscopes by hand, some magnifying up to 275 times. He had no formal scientific training and worked as a draper and surveyor. He discovered sperm cells, red blood cells, and many microorganisms. He wrote over 300 letters to the Royal Society describing his observations.', entity='called bacteria animalcules', question='What did Leeuwenhoek call the bacteria he first observed?', answer='animalcules', explanation='Leeuwenhoek was the first person to observe bacteria, which he called "animalcules."'),
        
        QAPair(topic='scientist', example='Gregor Mendel', passage='Mendel\'s work on inheritance was ignored during his lifetime and wasn\'t rediscovered until 1900, 16 years after his death. He studied seven characteristics of pea plants over eight years. He was an Augustinian friar who conducted experiments in the monastery garden. He also studied meteorology and kept bees. His laws of inheritance became the foundation of genetics.', entity='rediscovered in 1900', question='When was Mendel\'s work on genetics rediscovered?', answer='1900', explanation='Mendel\'s work was ignored during his lifetime and wasn\'t rediscovered until 1900, 16 years after his death.'),
        
        QAPair(topic='scientist', example='Charles Lyell', passage='Lyell\'s "Principles of Geology" influenced Darwin\'s thinking about evolution. He proposed that Earth was shaped by slow-moving forces over long periods, contradicting the prevailing belief in catastrophism. He coined the terms Eocene, Miocene, and Pliocene for geological epochs. Darwin took Lyell\'s book with him on the voyage of the Beagle.', entity='coined Eocene, Miocene, Pliocene', question='What geological epoch names did Charles Lyell coin?', answer='Eocene, Miocene, and Pliocene', explanation='Lyell coined the terms Eocene, Miocene, and Pliocene for geological epochs.'),
        
        QAPair(topic='scientist', example='Alfred Russel Wallace', passage='Wallace independently conceived the theory of evolution by natural selection while suffering from malaria in Indonesia. He sent his ideas to Darwin in 1858, prompting Darwin to finally publish "On the Origin of Species." Wallace is called the "father of biogeography" for his work on species distribution. The Wallace Line separates Asian and Australian fauna.', entity='conceived theory while having malaria', question='Under what circumstances did Wallace conceive his theory of evolution?', answer='while suffering from malaria in Indonesia', explanation='Wallace independently conceived the theory of evolution by natural selection while suffering from malaria in Indonesia.'),
        
        QAPair(topic='scientist', example='Dmitri Mendeleev', passage='Mendeleev reportedly conceived the periodic table in a dream after struggling with its organization for days. He left gaps for undiscovered elements and predicted their properties with remarkable accuracy. He was also an accomplished chess player and wrote extensively on economics. He died one day before his 73rd birthday, just missing the discovery of the noble gases.', entity='died one day before 73rd birthday', question='When did Mendeleev die in relation to his 73rd birthday?', answer='one day before his 73rd birthday', explanation='Mendeleev died one day before his 73rd birthday, just missing the discovery of the noble gases.'),
        
        QAPair(topic='scientist', example='Michael Faraday', passage='Faraday discovered electromagnetic induction, the principle behind electric generators and transformers. He had no formal mathematical training and couldn\'t understand his own equations - Maxwell later provided the mathematical framework. He declined a knighthood and refused to develop chemical weapons for the Crimean War. He gave popular Christmas lectures for children at the Royal Institution.', entity='no formal mathematical training', question='What educational limitation did Michael Faraday have despite his discoveries?', answer='no formal mathematical training', explanation='Faraday had no formal mathematical training and couldn\'t understand his own equations - Maxwell later provided the mathematical framework.'),
        
        QAPair(topic='scientist', example='James Clerk Maxwell', passage='Maxwell\'s equations unified electricity and magnetism and predicted the existence of electromagnetic waves. Einstein called Maxwell\'s work "the most profound and the most fruitful that physics has experienced since the time of Newton." He died of stomach cancer at age 48, the same age his mother died. He was the first person to produce a color photograph.', entity='first color photograph', question='What photographic first did James Clerk Maxwell achieve?', answer='first person to produce a color photograph', explanation='Maxwell was the first person to produce a color photograph, in addition to his groundbreaking work in physics.'),
        
        QAPair(topic='scientist', example='Lord Kelvin', passage='Kelvin developed the absolute temperature scale (Kelvin scale) where absolute zero is 0 K (-273.15°C). He calculated the age of Earth to be 20-40 million years old, which conflicted with Darwin\'s theory requiring much longer timescales. He famously said "heavier-than-air flying machines are impossible" just before the Wright brothers\' flight. He held 70 patents and was knighted for his work on the transatlantic telegraph cable.', entity='said flying machines impossible', question='What famous incorrect prediction did Lord Kelvin make about aviation?', answer='heavier-than-air flying machines are impossible', explanation='Kelvin famously said "heavier-than-air flying machines are impossible" just before the Wright brothers\' successful flight.'),
        
        QAPair(topic='scientist', example='Ernest Rutherford', passage='Rutherford discovered the atomic nucleus by firing alpha particles at gold foil and observing their scattering. He was the first to split an atom artificially in 1917. He identified and named alpha and beta radiation. He was known as the "father of nuclear physics." His students won 11 Nobel Prizes, more than any other scientist\'s students.', entity='students won 11 Nobel Prizes', question='How many Nobel Prizes did Rutherford\'s students win?', answer='11 Nobel Prizes', explanation='Rutherford\'s students won 11 Nobel Prizes, more than any other scientist\'s students, testament to his teaching ability.'),
        
        QAPair(topic='scientist', example='Niels Bohr', passage='Bohr developed the Bohr model of the atom with electrons in specific energy levels. He won the Nobel Prize in Physics in 1922. During WWII, he escaped Nazi-occupied Denmark in a fishing boat and later worked on the Manhattan Project. He advocated for peaceful uses of atomic energy after the war. Element 107, Bohrium, is named after him.', entity='escaped in fishing boat', question='How did Niels Bohr escape Nazi-occupied Denmark?', answer='in a fishing boat', explanation='During WWII, Bohr escaped Nazi-occupied Denmark in a fishing boat and later worked on the Manhattan Project.'),
        
        QAPair(topic='scientist', example='Max Planck', passage='Planck originated quantum theory in 1900, revolutionizing physics. He was initially reluctant to accept his own theory because it contradicted classical physics. He won the Nobel Prize in Physics in 1918. The Planck constant is fundamental to quantum mechanics. He lived through both World Wars and saw the rise of Nazi Germany, which he opposed.', entity='reluctant to accept own theory', question='What was Planck\'s initial reaction to his quantum theory?', answer='reluctant to accept it', explanation='Planck was initially reluctant to accept his own quantum theory because it contradicted established classical physics.'),
        
        QAPair(topic='scientist', example='Werner Heisenberg', passage='Heisenberg formulated the uncertainty principle, which states you cannot simultaneously know both position and momentum of a particle. He was only 25 when he developed matrix mechanics. He won the Nobel Prize in Physics in 1932. He led Germany\'s nuclear weapons program during WWII but may have deliberately sabotaged it. He was held by the Allies after the war.', entity='only 25 when developed matrix mechanics', question='How old was Heisenberg when he developed matrix mechanics?', answer='25', explanation='Heisenberg was only 25 years old when he developed matrix mechanics, a major formulation of quantum mechanics.'),
        
        QAPair(topic='scientist', example='Erwin Schrödinger', passage='Schrödinger developed wave mechanics and the famous Schrödinger equation. He proposed the thought experiment "Schrödinger\'s cat" to illustrate the absurdity of quantum superposition at macroscopic scales. He shared the 1933 Nobel Prize in Physics with Paul Dirac. He had a complex personal life with multiple relationships and illegitimate children.', entity='Schrödinger\'s cat thought experiment', question='What famous thought experiment did Schrödinger propose?', answer='Schrödinger\'s cat', explanation='Schrödinger proposed the "Schrödinger\'s cat" thought experiment to illustrate the absurdity of quantum superposition at macroscopic scales.'),
        
        QAPair(topic='scientist', example='Paul Dirac', passage='Dirac predicted the existence of antimatter through his relativistic quantum mechanics equations. He was known for his extreme quietness and precise speech. He shared the 1933 Nobel Prize with Schrödinger. He refused a knighthood because he didn\'t want to be called by his first name. The Dirac equation describes the behavior of fermions and predicted the positron.', entity='refused knighthood', question='Why did Paul Dirac refuse a knighthood?', answer='didn\'t want to be called by his first name', explanation='Dirac refused a knighthood because he didn\'t want to be called by his first name, reflecting his preference for formality.'),
    ]

if __name__ == "__main__":
    print("🚀 Expanding Self-Prompting ODQA Dataset from 137 to ~300 pairs...")
    
    # Get existing questions to avoid duplicates
    existing_questions, existing_examples = get_existing_questions()
    print(f"📊 Found {len(existing_questions)} existing questions to avoid duplicating")
    
    # Create additional questions
    politician_additions = create_additional_politician_questions()
    scientist_additions = create_additional_scientist_questions()
    
    print(f"✅ Created {len(politician_additions)} additional politician questions")
    print(f"✅ Created {len(scientist_additions)} additional scientist questions")
    
    # Check for duplicates
    duplicates_found = 0
    for qa_pair in politician_additions + scientist_additions:
        if qa_pair.question.lower().strip() in existing_questions:
            print(f"⚠️  Duplicate question found: {qa_pair.question[:50]}...")
            duplicates_found += 1
        if qa_pair.example.lower().strip() in existing_examples:
            print(f"⚠️  Duplicate example found: {qa_pair.example}")
            duplicates_found += 1
    
    if duplicates_found == 0:
        print("✅ No duplicates found - ready to add to database")
    else:
        print(f"❌ Found {duplicates_found} duplicates - need to review")
    
    print(f"\n📈 Progress so far:")
    print(f"  Politicians: 45 → {45 + len(politician_additions)} (+{len(politician_additions)})")
    print(f"  Scientists: 42 → {42 + len(scientist_additions)} (+{len(scientist_additions)})")
    print(f"  Total so far: 137 → {137 + len(politician_additions) + len(scientist_additions)}")
    print(f"\n⏳ Still need to create questions for:")
    print(f"  Geography: 10 → 45 (+35 needed)")
    print(f"  Countries: 10 → 45 (+35 needed)")
    print(f"  Literature: 10 → 45 (+35 needed)")
    print(f"  Technology: 10 → 45 (+35 needed)")
    print(f"  Historical Figures: 10 → 45 (+35 needed)")
    print(f"  Total remaining: 175 questions needed")
