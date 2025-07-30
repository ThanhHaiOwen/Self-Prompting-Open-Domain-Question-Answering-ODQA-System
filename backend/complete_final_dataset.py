#!/usr/bin/env python3
"""
Complete the final dataset by adding remaining politician and scientist questions
"""

import sys
sys.path.append('.')
from database import DatabaseManager, QAPair

def add_final_politician_questions():
    """Add 1 more politician question to reach 50+"""
    return [
        QAPair(topic='politician', example='Benazir Bhutto', passage='Benazir Bhutto was the first woman to lead a Muslim-majority country when she became Prime Minister of Pakistan in 1988. She was educated at Harvard and Oxford and spoke multiple languages fluently. She was assassinated in 2007 while campaigning for re-election. Her father, Zulfikar Ali Bhutto, was also a former Prime Minister who was executed in 1979.', entity='first woman to lead Muslim-majority country', question='What historic first did Benazir Bhutto achieve in 1988?', answer='first woman to lead a Muslim-majority country', explanation='Benazir Bhutto became the first woman to lead a Muslim-majority country when she became Prime Minister of Pakistan in 1988.'),
    ]

def add_final_scientist_questions():
    """Add 26 more scientist questions to reach 50+"""
    return [
        # More Medical Pioneers
        QAPair(topic='scientist', example='Joseph Lister', passage='Joseph Lister pioneered antiseptic surgery by using carbolic acid to sterilize surgical instruments and clean wounds. Before his methods, surgical mortality rates were as high as 50%. He was inspired by Louis Pasteur\'s germ theory and applied it to surgery. His techniques reduced post-operative infections dramatically and revolutionized surgery.', entity='carbolic acid', question='What substance did Joseph Lister use to pioneer antiseptic surgery?', answer='carbolic acid', explanation='Joseph Lister used carbolic acid to sterilize surgical instruments and clean wounds, pioneering antiseptic surgery.'),
        
        QAPair(topic='scientist', example='Paul Ehrlich', passage='Paul Ehrlich developed the first effective treatment for syphilis, called Salvarsan or "606" because it was the 606th compound he tested. He coined the term "magic bullet" for targeted drug therapy. He won the Nobel Prize in 1908 for his work on immunity. He also developed the first chemotherapy drugs for cancer treatment.', entity='606th compound', question='Why was Ehrlich\'s syphilis treatment called "606"?', answer='it was the 606th compound he tested', explanation='Ehrlich\'s syphilis treatment was called "606" because it was the 606th compound he tested before finding an effective one.'),
        
        QAPair(topic='scientist', example='Frederick Banting', passage='Frederick Banting discovered insulin in 1922, saving millions of diabetics\' lives. He was only 29 when he made the discovery and won the Nobel Prize at age 32, making him one of the youngest Nobel laureates. He sold the insulin patent to the University of Toronto for $1 to ensure it would be affordable. He died in a plane crash during WWII.', entity='sold patent for $1', question='How much did Frederick Banting sell the insulin patent for?', answer='$1', explanation='Banting sold the insulin patent to the University of Toronto for just $1 to ensure insulin would remain affordable for diabetics.'),
        
        # More Physics Pioneers
        QAPair(topic='scientist', example='Max Planck', passage='Max Planck originated quantum theory in 1900, which revolutionized physics. He was initially reluctant to accept his own theory because it contradicted classical physics. He won the Nobel Prize in 1918. The Planck constant is named after him and is fundamental to quantum mechanics. He lived through both World Wars and saw the rise of Nazi Germany.', entity='reluctant to accept own theory', question='What was Max Planck\'s initial reaction to his quantum theory?', answer='reluctant to accept it', explanation='Max Planck was initially reluctant to accept his own quantum theory because it contradicted established classical physics.'),
        
        QAPair(topic='scientist', example='Werner Heisenberg', passage='Werner Heisenberg formulated the uncertainty principle, which states that you cannot simultaneously know both the position and momentum of a particle. He was only 25 when he developed matrix mechanics, a formulation of quantum mechanics. He won the Nobel Prize in 1932. He led Germany\'s nuclear weapons program during WWII but may have deliberately sabotaged it.', entity='only 25', question='How old was Werner Heisenberg when he developed matrix mechanics?', answer='25', explanation='Heisenberg was only 25 years old when he developed matrix mechanics, a major formulation of quantum mechanics.'),
        
        QAPair(topic='scientist', example='Niels Bohr', passage='Niels Bohr developed the Bohr model of the atom and made fundamental contributions to quantum theory. He won the Nobel Prize in 1922. During WWII, he escaped Nazi-occupied Denmark in a fishing boat and later worked on the Manhattan Project. He advocated for peaceful uses of atomic energy after the war.', entity='escaped in fishing boat', question='How did Niels Bohr escape Nazi-occupied Denmark during WWII?', answer='in a fishing boat', explanation='Niels Bohr escaped Nazi-occupied Denmark during WWII by fleeing in a fishing boat.'),
        
        # More Chemistry Pioneers
        QAPair(topic='scientist', example='Alfred Nobel', passage='Alfred Nobel invented dynamite in 1867 and held 355 patents. He was called the "merchant of death" for his explosives, which troubled him. He established the Nobel Prizes in his will to be remembered for peace rather than destruction. He never married and had no children. He spoke five languages fluently.', entity='merchant of death', question='What troubling nickname was Alfred Nobel given during his lifetime?', answer='merchant of death', explanation='Alfred Nobel was called the "merchant of death" for his explosives inventions, which troubled him and influenced his decision to establish the Nobel Prizes.'),
        
        QAPair(topic='scientist', example='Fritz Haber', passage='Fritz Haber developed the process for synthesizing ammonia from nitrogen and hydrogen, which enabled mass production of fertilizers and explosives. His work feeds about half the world\'s population today. However, he also developed chemical weapons during WWI, earning him the nickname "father of chemical warfare." His wife, also a chemist, committed suicide in protest of his weapons work.', entity='wife committed suicide', question='How did Fritz Haber\'s wife react to his chemical weapons work?', answer='committed suicide in protest', explanation='Fritz Haber\'s wife, also a chemist, committed suicide in protest of his chemical weapons work during WWI.'),
        
        # More Biology Pioneers
        QAPair(topic='scientist', example='Lynn Margulis', passage='Lynn Margulis proposed the endosymbiotic theory, which explains how complex cells evolved from simpler ones. Her theory was initially rejected by the scientific community for 15 years before being accepted. She was married to astronomer Carl Sagan early in her career. She revolutionized our understanding of evolution and cellular biology.', entity='rejected for 15 years', question='How long was Lynn Margulis\'s endosymbiotic theory rejected by scientists?', answer='15 years', explanation='Lynn Margulis\'s endosymbiotic theory was initially rejected by the scientific community for 15 years before being accepted.'),
        
        QAPair(topic='scientist', example='James Watson', passage='James Watson co-discovered the structure of DNA at age 25 and won the Nobel Prize at 34. He later became controversial for his comments about race and intelligence. He was the first person to have his genome sequenced. He sold his Nobel Prize medal in 2014 for $4.1 million but later had it returned by the buyer.', entity='sold Nobel medal', question='What did James Watson do with his Nobel Prize medal in 2014?', answer='sold it for $4.1 million', explanation='James Watson sold his Nobel Prize medal in 2014 for $4.1 million, though it was later returned to him by the buyer.'),
        
        # More Women in Science
        QAPair(topic='scientist', example='Chien-Shiung Wu', passage='Chien-Shiung Wu conducted the Wu experiment that overthrew the law of conservation of parity in physics. However, her male colleagues won the Nobel Prize for the discovery while she was excluded. She was known as the "First Lady of Physics" and made fundamental contributions to nuclear physics. She worked on the Manhattan Project during WWII.', entity='excluded from Nobel Prize', question='What injustice did Chien-Shiung Wu face regarding the Nobel Prize?', answer='excluded while male colleagues won', explanation='Chien-Shiung Wu was excluded from the Nobel Prize for the Wu experiment while her male colleagues who theorized it won the prize.'),
        
        QAPair(topic='scientist', example='Lise Meitner', passage='Lise Meitner was the first to realize that uranium atoms were being split in nuclear fission, but her male colleague Otto Hahn received the Nobel Prize alone. She refused to work on the atomic bomb, saying she would "have nothing to do with a bomb." Element 109, Meitnerium, is named after her. She was called "the most significant woman scientist of the 20th century."', entity='refused atomic bomb work', question='What was Lise Meitner\'s stance on working on the atomic bomb?', answer='refused, saying she would have nothing to do with a bomb', explanation='Lise Meitner refused to work on the atomic bomb, stating she would "have nothing to do with a bomb."'),
        
        # More Modern Scientists
        QAPair(topic='scientist', example='Tim Berners-Lee', passage='Tim Berners-Lee invented the World Wide Web in 1989 while working at CERN. He chose not to patent his invention, giving it freely to humanity. He created the first web browser, web server, and website. He was knighted by Queen Elizabeth II in 2004. He continues to advocate for an open and free internet.', entity='chose not to patent', question='What decision did Tim Berners-Lee make about patenting the World Wide Web?', answer='chose not to patent it', explanation='Tim Berners-Lee chose not to patent the World Wide Web, giving his invention freely to humanity.'),
        
        QAPair(topic='scientist', example='Craig Venter', passage='Craig Venter led the private effort to sequence the human genome and competed with the public Human Genome Project. He created the first synthetic bacterial genome in 2010. He sailed around the world collecting marine microbes to study ocean biodiversity. He was one of the first people to have their complete genome sequenced.', entity='first synthetic bacterial genome', question='What biological first did Craig Venter achieve in 2010?', answer='created first synthetic bacterial genome', explanation='Craig Venter created the first synthetic bacterial genome in 2010, a major breakthrough in synthetic biology.'),
        
        # More Controversial Scientists
        QAPair(topic='scientist', example='Galileo Galilei', passage='Galileo was tried by the Inquisition for supporting heliocentrism and spent his last years under house arrest. He improved the telescope and discovered four moons of Jupiter. He allegedly said "And yet it moves" after being forced to recant his support for the heliocentric model. The Catholic Church didn\'t officially pardon him until 1992.', entity='pardoned in 1992', question='When did the Catholic Church officially pardon Galileo?', answer='1992', explanation='The Catholic Church didn\'t officially pardon Galileo for his support of heliocentrism until 1992, over 350 years after his trial.'),
        
        QAPair(topic='scientist', example='Ignaz Semmelweis', passage='Ignaz Semmelweis discovered that handwashing dramatically reduced mortality in maternity wards, but his ideas were rejected by the medical establishment. He was eventually committed to an asylum where he died, possibly beaten by guards. His ideas weren\'t accepted until after Pasteur\'s germ theory gained acceptance. He\'s now known as the "savior of mothers."', entity='committed to asylum', question='What tragic fate befell Ignaz Semmelweis for his handwashing advocacy?', answer='committed to an asylum where he died', explanation='Ignaz Semmelweis was committed to an asylum for his persistent advocacy of handwashing and died there, possibly beaten by guards.'),
        
        # More Mathematicians
        QAPair(topic='scientist', example='Alan Turing', passage='Alan Turing broke the Enigma code during WWII, helping to shorten the war by an estimated 2-4 years. He laid the theoretical foundation for computer science and artificial intelligence. He was prosecuted for homosexuality in 1952 and underwent chemical castration. He died in 1954, possibly by suicide, though some believe it was accidental.', entity='shortened war 2-4 years', question='How much did Turing\'s code-breaking work help shorten WWII?', answer='estimated 2-4 years', explanation='Alan Turing\'s work breaking the Enigma code is estimated to have shortened WWII by 2-4 years.'),
        
        QAPair(topic='scientist', example='Srinivasa Ramanujan', passage='Srinivasa Ramanujan was a self-taught Indian mathematician who made extraordinary contributions to number theory. He had no formal training but produced nearly 4,000 mathematical results. He claimed his insights came to him in dreams from the Hindu goddess Namagiri. He died at age 32 from illness, possibly tuberculosis.', entity='insights from goddess in dreams', question='How did Ramanujan claim to receive his mathematical insights?', answer='in dreams from the Hindu goddess Namagiri', explanation='Ramanujan claimed his mathematical insights came to him in dreams from the Hindu goddess Namagiri.'),
        
        # More Astronomers
        QAPair(topic='scientist', example='Edwin Hubble', passage='Edwin Hubble discovered that the universe is expanding, leading to the Big Bang theory. The Hubble Space Telescope is named after him. He was also a skilled athlete and boxer in his youth. He served in WWI and was wounded in action. He initially studied law before switching to astronomy.', entity='studied law initially', question='What did Edwin Hubble study before switching to astronomy?', answer='law', explanation='Edwin Hubble initially studied law before switching to astronomy and making his groundbreaking discoveries about the expanding universe.'),
        
        QAPair(topic='scientist', example='Carl Sagan', passage='Carl Sagan popularized science through his TV series "Cosmos" and the novel "Contact." He helped design the Pioneer plaques and Voyager Golden Records sent into space. He was a strong advocate for the search for extraterrestrial intelligence (SETI). He coined the phrase "billions and billions" though he claimed he never actually said it that way.', entity='never said billions and billions', question='What famous phrase is associated with Carl Sagan that he claimed he never said?', answer='billions and billions', explanation='Carl Sagan is associated with the phrase "billions and billions" though he claimed he never actually said it that way.'),
        
        # More Environmental Scientists
        QAPair(topic='scientist', example='Jane Goodall', passage='Jane Goodall revolutionized the study of chimpanzees by observing them in the wild for over 60 years. She discovered that chimps use tools, which redefined what it means to be human. She had no formal scientific training when she started but earned a PhD from Cambridge. She was sent to Africa by Louis Leakey when she was just 26.', entity='no formal training initially', question='What was unusual about Jane Goodall\'s scientific background when she started?', answer='had no formal scientific training', explanation='Jane Goodall had no formal scientific training when she started her groundbreaking chimpanzee research, later earning a PhD from Cambridge.'),
        
        QAPair(topic='scientist', example='Dian Fossey', passage='Dian Fossey studied mountain gorillas in Rwanda for 18 years and was murdered in 1985, likely for her anti-poaching efforts. She habituated gorillas to human presence and gave them names instead of numbers. Her work was featured in the film "Gorillas in the Mist." She was initially an occupational therapist before becoming a primatologist.', entity='murdered for anti-poaching', question='Why was Dian Fossey likely murdered in 1985?', answer='for her anti-poaching efforts', explanation='Dian Fossey was likely murdered in 1985 for her aggressive anti-poaching efforts to protect mountain gorillas.'),
        
        # More Computer Scientists
        QAPair(topic='scientist', example='Ada Lovelace', passage='Ada Lovelace wrote the first computer program in 1843 for Charles Babbage\'s Analytical Engine. She was the daughter of poet Lord Byron and had a talent for both mathematics and poetry. She envisioned computers being used for more than just calculations, including music and art. She died at age 36 from uterine cancer.', entity='first computer program 1843', question='When did Ada Lovelace write the first computer program?', answer='1843', explanation='Ada Lovelace wrote the first computer program in 1843 for Charles Babbage\'s Analytical Engine.'),
        
        QAPair(topic='scientist', example='Grace Hopper', passage='Grace Hopper developed the first compiler for a computer programming language and helped develop COBOL. She popularized the term "computer bug" after finding an actual moth stuck in a computer relay. She was a U.S. Navy rear admiral and worked on the Harvard Mark I computer. She was known as "Amazing Grace" for her pioneering work.', entity='actual moth in relay', question='How did Grace Hopper popularize the term "computer bug"?', answer='found an actual moth stuck in a computer relay', explanation='Grace Hopper popularized the term "computer bug" after finding an actual moth stuck in a computer relay.'),
        
        # More Geneticists
        QAPair(topic='scientist', example='Francis Collins', passage='Francis Collins led the Human Genome Project and later became director of the National Institutes of Health. He is an evangelical Christian who sees no conflict between science and faith. He founded the BioLogos Foundation to promote harmony between science and Christianity. He also led the effort to sequence the genomes of several diseases.', entity='evangelical Christian scientist', question='What makes Francis Collins unusual among prominent scientists?', answer='evangelical Christian who sees no conflict with science', explanation='Francis Collins is unusual as a prominent scientist who is an evangelical Christian and sees no conflict between science and faith.'),
        
        QAPair(topic='scientist', example='Jennifer Doudna', passage='Jennifer Doudna co-developed CRISPR gene editing technology, which allows precise editing of DNA. She won the Nobel Prize in Chemistry in 2020, sharing it with Emmanuelle Charpentier. She initially studied RNA structure before moving into gene editing. She has expressed concerns about the ethical implications of her technology.', entity='expressed ethical concerns', question='What is Jennifer Doudna\'s stance on the implications of CRISPR technology?', answer='expressed concerns about ethical implications', explanation='Jennifer Doudna has expressed concerns about the ethical implications of the CRISPR gene editing technology she helped develop.'),
    ]

if __name__ == "__main__":
    db = DatabaseManager()
    
    # Add final questions
    politician_final = add_final_politician_questions()
    scientist_final = add_final_scientist_questions()
    
    print(f"--- Adding {len(politician_final)} final politician question ---")
    for qa_pair in politician_final:
        try:
            qa_id = db.save_qa_pair(qa_pair)
            print(f'Added politician QA pair: {qa_pair.question[:70]}... (ID: {qa_id})')
        except Exception as e:
            print(f'Error inserting QA pair: {e}')
    
    print(f"\n--- Adding {len(scientist_final)} final scientist questions ---")
    for i, qa_pair in enumerate(scientist_final):
        try:
            qa_id = db.save_qa_pair(qa_pair)
            if i < 5:
                print(f'Added scientist QA pair: {qa_pair.question[:70]}... (ID: {qa_id})')
            elif i == 5:
                print(f'... (continuing to add {len(scientist_final) - 5} more scientist questions)')
        except Exception as e:
            print(f'Error inserting QA pair: {e}')
    
    # Show final statistics
    stats = db.get_dataset_stats()
    print(f'\n🎉 FINAL COMPLETE DATASET STATISTICS:')
    for topic, count in stats['topic_counts'].items():
        status = "✅" if count >= 50 else "❌"
        print(f'  {status} {topic}: {count} pairs')
    print(f'  📊 Total: {stats["total_pairs"]} pairs')
    
    # Check if all topics have 50+ questions
    all_sufficient = all(count >= 50 for count in stats['topic_counts'].values())
    if all_sufficient:
        print(f'\n🎯 SUCCESS: All 7 topics now have 50+ authentic, diverse questions!')
        print(f'✅ Dataset is complete and ready for use!')
    else:
        insufficient = [topic for topic, count in stats['topic_counts'].items() if count < 50]
        print(f'\n❌ Topics still needing expansion: {", ".join(insufficient)}')
