#!/usr/bin/env python3
"""
Add first batch of completely unique questions to expand dataset
"""

import sys
sys.path.append('.')
from database import DatabaseManager, QAPair

def add_unique_politician_questions():
    """20 politician questions with completely new examples"""
    return [
        QAPair(topic='politician', example='Lyndon B. Johnson', passage='LBJ was sworn in as president aboard Air Force One just 99 minutes after Kennedy\'s assassination. He was known for his "Johnson Treatment" - physically intimidating senators by getting very close to them during conversations. He was 6\'4" tall and would lean over senators to pressure them. He chose not to run for re-election in 1968 due to the Vietnam War.', entity='Johnson Treatment', question='What intimidation technique was LBJ known for using on senators?', answer='Johnson Treatment - getting very close to intimidate them', explanation='LBJ was known for his "Johnson Treatment" - physically intimidating senators by getting very close to them during conversations.'),
        
        QAPair(topic='politician', example='Harry S. Truman', passage='Truman\'s middle initial "S" doesn\'t stand for any specific name - it honors both his grandfathers. He was a failed haberdasher before entering politics and went bankrupt. He made the decision to drop atomic bombs on Japan without consulting Congress. His approval rating dropped to 22% in 1952, one of the lowest in presidential history.', entity='failed haberdasher', question='What business did Harry Truman fail at before entering politics?', answer='haberdasher', explanation='Truman was a failed haberdasher before entering politics and went bankrupt in the business.'),
        
        QAPair(topic='politician', example='Chester A. Arthur', passage='Arthur became president after James Garfield\'s assassination and was known for his elegant style. He was called "Elegant Arthur" and owned 80 pairs of pants. He completely redecorated the White House, selling 24 wagonloads of furniture. He signed the Pendleton Civil Service Act, creating a merit-based system for federal jobs.', entity='sold 24 wagonloads of furniture', question='How much White House furniture did Chester Arthur sell during redecorating?', answer='24 wagonloads', explanation='Arthur completely redecorated the White House, selling 24 wagonloads of furniture in the process.'),
        
        QAPair(topic='politician', example='Benjamin Harrison', passage='Harrison was the grandson of William Henry Harrison, making them the only grandfather-grandson presidential pair. He was the first president to use electric lights in the White House but was afraid to touch the switches. He lost the popular vote but won the electoral college. He was known for his cold personality and was called the "Human Iceberg."', entity='Human Iceberg', question='What nickname did Benjamin Harrison earn due to his personality?', answer='Human Iceberg', explanation='Harrison was known for his cold personality and was called the "Human Iceberg."'),
        
        QAPair(topic='politician', example='Rutherford B. Hayes', passage='Hayes won the presidency in the most disputed election in U.S. history, decided by a 15-member electoral commission. He was the first president to use a telephone in the White House, with the number "1." His wife Lucy banned alcohol from the White House, earning her the nickname "Lemonade Lucy." He promised to serve only one term and kept his word.', entity='telephone number 1', question='What was the White House telephone number when Hayes first used one?', answer='1', explanation='Hayes was the first president to use a telephone in the White House, and the number was simply "1."'),
        
        QAPair(topic='politician', example='James A. Garfield', passage='Garfield could write Latin with one hand and Greek with the other simultaneously. He was shot by Charles J. Guiteau after only 200 days in office and died 79 days later from infections caused by doctors\' unsanitary treatment. He was the last president born in a log cabin and the first left-handed president.', entity='first left-handed president', question='What handedness distinction does James Garfield hold among presidents?', answer='first left-handed president', explanation='Garfield was the first left-handed president in U.S. history.'),
        
        QAPair(topic='politician', example='Ulysses S. Grant', passage='Grant\'s real first name was Hiram, but a clerical error at West Point changed it to Ulysses. He was a heavy drinker and chain smoker who went through 20 cigars a day. He wrote his memoirs while dying of throat cancer to provide for his family, finishing them just days before his death. The memoirs became a bestseller.', entity='real name Hiram', question='What was Ulysses S. Grant\'s real first name?', answer='Hiram', explanation='Grant\'s real first name was Hiram, but a clerical error at West Point changed it to Ulysses.'),
        
        QAPair(topic='politician', example='Andrew Johnson', passage='Johnson was the first president to be impeached by the House of Representatives. He was a tailor before entering politics and made his own clothes throughout his life. He never attended school and his wife taught him to read and write. He was drunk during his vice-presidential inauguration speech.', entity='was a tailor', question='What was Andrew Johnson\'s profession before entering politics?', answer='tailor', explanation='Johnson was a tailor before entering politics and made his own clothes throughout his life.'),
        
        QAPair(topic='politician', example='Franklin Pierce', passage='Pierce was the only president from New Hampshire and the only elected president to serve his full term without making any changes to his cabinet. He was arrested while president for running over an old woman with his horse, but charges were dropped. His son was killed in a train accident just before his inauguration.', entity='only president from New Hampshire', question='What state distinction does Franklin Pierce hold among presidents?', answer='only president from New Hampshire', explanation='Pierce was the only president from New Hampshire in U.S. history.'),
        
        QAPair(topic='politician', example='Millard Fillmore', passage='Fillmore installed the first bathtub and kitchen stove in the White House. He was never elected president - he became president when Zachary Taylor died. He sent Commodore Perry to open trade with Japan. After his presidency, he was nominated by the Know-Nothing Party in 1856. He founded the University at Buffalo.', entity='founded University at Buffalo', question='What university did Millard Fillmore found?', answer='University at Buffalo', explanation='Fillmore founded the University at Buffalo after his presidency.'),
        
        QAPair(topic='politician', example='Zachary Taylor', passage='Taylor was a career military officer who never voted in a presidential election before becoming president himself. He owned a plantation with over 100 slaves but opposed the expansion of slavery. He died after 16 months in office, possibly from gastroenteritis after consuming large quantities of cold milk and cherries on July 4th.', entity='died from milk and cherries', question='What foods may have contributed to Zachary Taylor\'s death?', answer='cold milk and cherries', explanation='Taylor died possibly from gastroenteritis after consuming large quantities of cold milk and cherries on July 4th.'),
        
        QAPair(topic='politician', example='James K. Polk', passage='Polk promised to serve only one term and kept his word. He achieved all four of his campaign goals: lowering tariffs, establishing an independent treasury, settling the Oregon boundary, and acquiring California. He expanded the U.S. by about one-third through the Mexican-American War. He worked so hard that he died just 103 days after leaving office.', entity='achieved all four campaign goals', question='How many of his campaign goals did James K. Polk achieve?', answer='all four', explanation='Polk achieved all four of his campaign goals: lowering tariffs, establishing an independent treasury, settling the Oregon boundary, and acquiring California.'),
        
        QAPair(topic='politician', example='John Tyler', passage='Tyler was expelled from his own Whig Party while serving as president, earning him the nickname "His Accidency." He had 15 children with two wives - more than any other president. His 10th child was born when he was 63. He later served in the Confederate Congress during the Civil War.', entity='His Accidency', question='What nickname did John Tyler earn from his own party?', answer='His Accidency', explanation='Tyler was expelled from his own Whig Party while serving as president, earning him the nickname "His Accidency."'),
        
        QAPair(topic='politician', example='Martin Van Buren', passage='Van Buren was the first president born as a U.S. citizen (previous presidents were born as British subjects). He was known as "Old Kinderhook" and his supporters were called "O.K.," which may be the origin of the term "okay." He spoke Dutch as his first language and didn\'t learn English until he was a teenager.', entity='spoke Dutch first', question='What was Martin Van Buren\'s first language?', answer='Dutch', explanation='Van Buren spoke Dutch as his first language and didn\'t learn English until he was a teenager.'),
        
        QAPair(topic='politician', example='William Henry Harrison', passage='Harrison gave the longest inaugural address in history - 8,445 words lasting nearly two hours in cold, wet weather without a coat or hat. He died of pneumonia 31 days later, making his the shortest presidency. His grandson Benjamin Harrison also became president. He was the last president born as a British subject.', entity='last born as British subject', question='What birth distinction does William Henry Harrison hold among presidents?', answer='last president born as a British subject', explanation='Harrison was the last president born as a British subject before American independence.'),
        
        QAPair(topic='politician', example='James Madison', passage='Madison was the shortest president at 5 feet 4 inches and weighed about 100 pounds. He was called the "Father of the Constitution" for his role in drafting it. He was the first president to wear long pants instead of knee breeches. During the War of 1812, he became the only president to lead troops in battle while in office.', entity='first to wear long pants', question='What fashion first did James Madison introduce as president?', answer='first to wear long pants instead of knee breeches', explanation='Madison was the first president to wear long pants instead of knee breeches.'),
        
        QAPair(topic='politician', example='James Monroe', passage='Monroe was the last president who was a Founding Father and the last to wear a powdered wig. His presidency was called the "Era of Good Feelings" because there was little partisan conflict. He established the Monroe Doctrine, warning European powers not to interfere in the Americas. He died on July 4, 1831.', entity='last to wear powdered wig', question='What grooming distinction does James Monroe hold among presidents?', answer='last to wear a powdered wig', explanation='Monroe was the last president to wear a powdered wig, marking the end of an era.'),
        
        QAPair(topic='politician', example='Hubert Humphrey', passage='Humphrey was known as the "Happy Warrior" for his optimistic demeanor and liberal politics. He was the first pharmacist to become Vice President. He gave a famous speech at the 1948 Democratic Convention that helped integrate the party. He lost the 1968 presidential election to Nixon by less than 1% of the popular vote.', entity='Happy Warrior', question='What nickname did Hubert Humphrey earn for his demeanor?', answer='Happy Warrior', explanation='Humphrey was known as the "Happy Warrior" for his optimistic demeanor and liberal politics.'),
        
        QAPair(topic='politician', example='Strom Thurmond', passage='Thurmond holds the record for the longest filibuster in U.S. Senate history, speaking for 24 hours and 18 minutes against the Civil Rights Act of 1957. He was 100 years old when he retired from the Senate in 2003, making him the oldest serving senator in history. He switched from Democrat to Republican in 1964.', entity='oldest serving senator', question='What age record does Strom Thurmond hold in the Senate?', answer='oldest serving senator at 100 years old', explanation='Thurmond was 100 years old when he retired from the Senate in 2003, making him the oldest serving senator in history.'),
        
        QAPair(topic='politician', example='Robert Byrd', passage='Byrd served in the U.S. Senate for over 51 years, longer than anyone in history. He was a former member of the Ku Klux Klan, which he later called the greatest mistake of his life. He was known as the "King of Pork" for bringing federal projects to West Virginia. He memorized the entire Constitution and often quoted it on the Senate floor.', entity='King of Pork', question='What nickname did Robert Byrd earn for his legislative style?', answer='King of Pork', explanation='Byrd was known as the "King of Pork" for bringing federal projects to West Virginia during his 51-year Senate career.'),
    ]

def add_unique_scientist_questions():
    """18 scientist questions with completely new examples"""
    return [
        QAPair(topic='scientist', example='Robert Hooke', passage='Hooke coined the term "cell" after observing cork under a microscope - the structures reminded him of monastery cells. He formulated Hooke\'s Law of elasticity and designed many of London\'s buildings after the Great Fire of 1666. He had a bitter rivalry with Newton over credit for the inverse square law of gravitation. He was also an accomplished architect.', entity='designed London buildings', question='What did Robert Hooke design after the Great Fire of 1666?', answer='many of London\'s buildings', explanation='Hooke designed many of London\'s buildings after the Great Fire of 1666, in addition to his scientific work.'),
        
        QAPair(topic='scientist', example='Antonie van Leeuwenhoek', passage='Leeuwenhoek was the first person to observe bacteria, which he called "animalcules." He made over 500 microscopes by hand, some magnifying up to 275 times. He had no formal scientific training and worked as a draper and surveyor. He wrote over 300 letters to the Royal Society describing his observations.', entity='made 500 microscopes by hand', question='How many microscopes did Leeuwenhoek make by hand?', answer='over 500', explanation='Leeuwenhoek made over 500 microscopes by hand, some magnifying up to 275 times.'),
        
        QAPair(topic='scientist', example='Johannes Kepler', passage='Kepler discovered that planets orbit the sun in ellipses, not perfect circles as previously believed. His mother was accused of witchcraft and he spent six years defending her in court. He worked as an assistant to Tycho Brahe and inherited his precise astronomical data. He believed that the planets made music as they moved through space.', entity='planets made music', question='What unusual belief did Kepler have about planetary motion?', answer='planets made music as they moved through space', explanation='Kepler believed that the planets made music as they moved through space, a concept called "music of the spheres."'),
        
        QAPair(topic='scientist', example='Tycho Brahe', passage='Brahe lost part of his nose in a duel and wore a prosthetic nose made of gold and silver for the rest of his life. He owned a pet elk that died after drinking too much beer at a dinner party. He made the most accurate astronomical observations before the telescope was invented. He discovered a supernova in 1572.', entity='pet elk died from beer', question='How did Tycho Brahe\'s pet elk die?', answer='drinking too much beer at a dinner party', explanation='Brahe owned a pet elk that died after drinking too much beer at a dinner party.'),
        
        QAPair(topic='scientist', example='William Harvey', passage='Harvey discovered the circulation of blood in the human body, overturning 1,400 years of medical belief. He was physician to King Charles I and performed the first recorded autopsy on a human heart. He was accused of being a "circulator" - a derogatory term for someone who spread new ideas. He lived to age 79, remarkable for the 17th century.', entity='accused of being circulator', question='What derogatory term was William Harvey called for his discoveries?', answer='circulator', explanation='Harvey was accused of being a "circulator" - a derogatory term for someone who spread new ideas about blood circulation.'),
        
        QAPair(topic='scientist', example='Andreas Vesalius', passage='Vesalius revolutionized anatomy by performing dissections himself rather than reading from ancient texts. He corrected over 200 errors in Galen\'s anatomical work, which had been accepted for 1,300 years. He was condemned by the Church for his work and died on a pilgrimage to the Holy Land. He published "De Humani Corporis Fabrica" at age 28.', entity='corrected 200 errors in Galen', question='How many errors did Vesalius correct in Galen\'s anatomical work?', answer='over 200', explanation='Vesalius corrected over 200 errors in Galen\'s anatomical work, which had been accepted for 1,300 years.'),
        
        QAPair(topic='scientist', example='Paracelsus', passage='Paracelsus was a Swiss physician who pioneered the use of chemicals and minerals in medicine. He burned the books of Galen and Avicenna publicly, declaring that his shoe buckles knew more than they did. He coined the phrase "the dose makes the poison." He was one of the first to suggest that diseases were caused by external agents, not imbalances of bodily humors.', entity='shoe buckles knew more', question='What did Paracelsus claim his shoe buckles knew more than?', answer='the books of Galen and Avicenna', explanation='Paracelsus burned the books of Galen and Avicenna publicly, declaring that his shoe buckles knew more than they did.'),
        
        QAPair(topic='scientist', example='Robert Koch', passage='Koch identified the specific bacteria that cause tuberculosis, cholera, and anthrax. He developed Koch\'s postulates, which are still used to identify disease-causing organisms. He won the Nobel Prize in Medicine in 1905. He was the first to use solid media to grow bacteria, revolutionizing microbiology. He photographed bacteria through microscopes.', entity='first to photograph bacteria', question='What photographic first did Robert Koch achieve in microbiology?', answer='first to photograph bacteria through microscopes', explanation='Koch was the first to photograph bacteria through microscopes, revolutionizing the documentation of microbiology.'),
        
        QAPair(topic='scientist', example='Alexander Fleming', passage='Fleming discovered penicillin by accident in 1928 when a mold contaminated his bacterial culture plates. He initially called the substance "mold juice" before naming it penicillin. However, he couldn\'t figure out how to mass-produce it. It wasn\'t until Howard Florey and Ernst Boris Chain developed production methods that penicillin became widely available.', entity='called it mold juice', question='What did Fleming initially call penicillin when he first discovered it?', answer='mold juice', explanation='Fleming initially called his discovery "mold juice" before giving it the more scientific name penicillin.'),
        
        QAPair(topic='scientist', example='Edward Jenner', passage='Jenner created the first vaccine by using cowpox to prevent smallpox in 1796. He tested it first on his gardener\'s 8-year-old son, James Phipps. The word "vaccine" comes from "vacca," the Latin word for cow. His work led to the complete eradication of smallpox—the only human disease ever eliminated. He was initially ridiculed by the medical establishment.', entity='tested on gardener\'s son', question='Who was the first person Jenner tested his smallpox vaccine on?', answer='his gardener\'s 8-year-old son James Phipps', explanation='Jenner first tested his smallpox vaccine on James Phipps, his gardener\'s 8-year-old son, in 1796.'),
        
        QAPair(topic='scientist', example='Wilhelm Röntgen', passage='Röntgen discovered X-rays accidentally in 1895 while experimenting with cathode rays. The first X-ray image was of his wife\'s hand, showing her wedding ring. He refused to patent his discovery, believing it should benefit all humanity. He won the first Nobel Prize in Physics in 1901. He called them "X-rays" because he didn\'t understand what they were—X meaning unknown.', entity='first X-ray of wife\'s hand', question='What was the subject of the first X-ray image ever taken?', answer='his wife\'s hand showing her wedding ring', explanation='The first X-ray image was of Röntgen\'s wife\'s hand, clearly showing her wedding ring and bones.'),
        
        QAPair(topic='scientist', example='Antoine Lavoisier', passage='Lavoisier is called the "Father of Modern Chemistry" for establishing the law of conservation of mass. He named oxygen and hydrogen and helped create the metric system. He was executed during the French Revolution in 1794 at age 50. The judge reportedly said "The Republic needs neither scientists nor chemists." His wife Marie-Anne was also a chemist and illustrated his work.', entity='executed during French Revolution', question='How did Lavoisier die?', answer='executed during French Revolution', explanation='Lavoisier was executed by guillotine during the French Revolution in 1794, with the judge saying "The Republic needs neither scientists nor chemists."'),
        
        QAPair(topic='scientist', example='Dorothy Hodgkin', passage='Hodgkin won the Nobel Prize in Chemistry in 1964 for determining the structure of vitamin B12 using X-ray crystallography. She was the third woman to win a Nobel Prize in science and the only British woman to win a Nobel in science. She suffered from severe rheumatoid arthritis but continued her research despite painful, deformed hands. She also determined the structure of penicillin and insulin.', entity='only British woman Nobel science', question='What distinction does Dorothy Hodgkin hold among British Nobel laureates?', answer='only British woman to win Nobel in science', explanation='Dorothy Hodgkin is the only British woman to win a Nobel Prize in science, winning Chemistry in 1964.'),
        
        QAPair(topic='scientist', example='Paul Ehrlich', passage='Paul Ehrlich developed the first effective treatment for syphilis, called Salvarsan or "606" because it was the 606th compound he tested. He coined the term "magic bullet" for targeted drug therapy. He won the Nobel Prize in 1908 for his work on immunity. He also developed the first chemotherapy drugs for cancer treatment.', entity='606th compound', question='Why was Ehrlich\'s syphilis treatment called "606"?', answer='it was the 606th compound he tested', explanation='Ehrlich\'s syphilis treatment was called "606" because it was the 606th compound he tested before finding an effective one.'),
        
        QAPair(topic='scientist', example='Frederick Banting', passage='Frederick Banting discovered insulin in 1922, saving millions of diabetics\' lives. He was only 29 when he made the discovery and won the Nobel Prize at age 32, making him one of the youngest Nobel laureates. He sold the insulin patent to the University of Toronto for $1 to ensure it would be affordable. He died in a plane crash during WWII.', entity='sold patent for $1', question='How much did Frederick Banting sell the insulin patent for?', answer='$1', explanation='Banting sold the insulin patent to the University of Toronto for just $1 to ensure insulin would remain affordable for diabetics.'),
        
        QAPair(topic='scientist', example='Alfred Nobel', passage='Alfred Nobel invented dynamite in 1867 and held 355 patents. He was called the "merchant of death" for his explosives, which troubled him. He established the Nobel Prizes in his will to be remembered for peace rather than destruction. He never married and had no children. He spoke five languages fluently.', entity='merchant of death', question='What troubling nickname was Alfred Nobel given during his lifetime?', answer='merchant of death', explanation='Alfred Nobel was called the "merchant of death" for his explosives inventions, which troubled him and influenced his decision to establish the Nobel Prizes.'),
        
        QAPair(topic='scientist', example='Fritz Haber', passage='Fritz Haber developed the process for synthesizing ammonia from nitrogen and hydrogen, which enabled mass production of fertilizers and explosives. His work feeds about half the world\'s population today. However, he also developed chemical weapons during WWI, earning him the nickname "father of chemical warfare." His wife, also a chemist, committed suicide in protest of his weapons work.', entity='wife committed suicide', question='How did Fritz Haber\'s wife react to his chemical weapons work?', answer='committed suicide in protest', explanation='Fritz Haber\'s wife, also a chemist, committed suicide in protest of his chemical weapons work during WWI.'),
        
        QAPair(topic='scientist', example='Lynn Margulis', passage='Lynn Margulis proposed the endosymbiotic theory, which explains how complex cells evolved from simpler ones. Her theory was initially rejected by the scientific community for 15 years before being accepted. She was married to astronomer Carl Sagan early in her career. She revolutionized our understanding of evolution and cellular biology.', entity='rejected for 15 years', question='How long was Lynn Margulis\'s endosymbiotic theory rejected by scientists?', answer='15 years', explanation='Lynn Margulis\'s endosymbiotic theory was initially rejected by the scientific community for 15 years before being accepted.'),
    ]

if __name__ == "__main__":
    print("🚀 Adding first batch of completely unique questions...")
    
    # Get existing data
    db = DatabaseManager()
    existing_pairs = db.get_qa_pairs()
    existing_questions = set(p.question.lower().strip() for p in existing_pairs)
    existing_examples = set(p.example.lower().strip() for p in existing_pairs)
    current_total = len(existing_pairs)
    
    print(f"📊 Current dataset: {current_total} QA pairs")
    
    # Create new questions
    politician_additions = add_unique_politician_questions()
    scientist_additions = add_unique_scientist_questions()
    
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
        print("✅ No duplicates found - adding to database!")
        
        # Add to database
        added_count = 0
        for qa_pair in politician_additions + scientist_additions:
            try:
                qa_id = db.save_qa_pair(qa_pair)
                added_count += 1
                if added_count <= 5:
                    print(f"  ✓ Added: {qa_pair.question[:50]}... (ID: {qa_id})")
            except Exception as e:
                print(f"❌ Error adding question: {e}")
        
        print(f"✅ Successfully added {added_count} new questions to database")
        
        # Show updated stats
        updated_stats = db.get_dataset_stats()
        print(f"\n📊 Updated Dataset Statistics:")
        for topic, count in updated_stats['topic_counts'].items():
            print(f"  {topic}: {count} pairs")
        print(f"  Total: {updated_stats['total_pairs']} pairs")
        
        print(f"\n🎯 Progress toward 300 total:")
        remaining = 300 - updated_stats['total_pairs']
        print(f"  Current: {updated_stats['total_pairs']}")
        print(f"  Target: 300")
        print(f"  Remaining: {remaining}")
        
    else:
        print(f"❌ Found {duplicates_found} duplicates - need to fix before adding")
