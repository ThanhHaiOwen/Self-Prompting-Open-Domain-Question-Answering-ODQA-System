#!/usr/bin/env python3
"""
Create a sample dataset with 300 QA pairs for the Self-Prompting ODQA system
"""

import sys
import os
sys.path.append('backend')

from backend.database import DatabaseManager, QAPair
import numpy as np
from sentence_transformers import SentenceTransformer

# Sample QA pairs organized by topics
SAMPLE_QA_PAIRS = [
    # Politicians (30 pairs)
    ("Who was the first President of the United States?", "George Washington", "politician", "George Washington", "George Washington was the first President of the United States, serving from 1789 to 1797."),
    ("Who is the current President of France?", "Emmanuel Macron", "politician", "Emmanuel Macron", "Emmanuel Macron has been serving as President of France since 2017."),
    ("Which British Prime Minister led the country during World War II?", "Winston Churchill", "politician", "Winston Churchill", "Winston Churchill served as Prime Minister during most of World War II from 1940 to 1945."),
    ("Who was the longest-serving US President?", "Franklin D. Roosevelt", "politician", "Franklin D. Roosevelt", "FDR served as President for over 12 years from 1933 until his death in 1945."),
    ("Which President appears on Mount Rushmore alongside Washington, Jefferson, and Roosevelt?", "Abraham Lincoln", "politician", "Abraham Lincoln", "Abraham Lincoln is one of the four presidents carved into Mount Rushmore."),
    ("Who was the first female Prime Minister of the United Kingdom?", "Margaret Thatcher", "politician", "Margaret Thatcher", "Margaret Thatcher served as Prime Minister from 1979 to 1990."),
    ("Which US President was involved in the Watergate scandal?", "Richard Nixon", "politician", "Richard Nixon", "Richard Nixon resigned from the presidency in 1974 due to the Watergate scandal."),
    ("Who was the youngest elected US President?", "John F. Kennedy", "politician", "John F. Kennedy", "JFK was 43 years old when he was elected President in 1960."),
    ("Which German Chancellor reunified East and West Germany?", "Helmut Kohl", "politician", "Helmut Kohl", "Helmut Kohl served as Chancellor during German reunification in 1990."),
    ("Who was the first African American President of the United States?", "Barack Obama", "politician", "Barack Obama", "Barack Obama served as the 44th President from 2009 to 2017."),
    
    # Athletes (25 pairs)
    ("Who holds the record for most Olympic gold medals?", "Michael Phelps", "athlete", "Michael Phelps", "Michael Phelps won 23 Olympic gold medals in swimming."),
    ("Which tennis player has won the most Grand Slam singles titles?", "Novak Djokovic", "athlete", "Novak Djokovic", "Novak Djokovic has won 24 Grand Slam singles titles as of 2023."),
    ("Who is considered the greatest basketball player of all time?", "Michael Jordan", "athlete", "Michael Jordan", "Michael Jordan won 6 NBA championships with the Chicago Bulls."),
    ("Which footballer has scored the most goals in World Cup history?", "Miroslav Klose", "athlete", "Miroslav Klose", "Miroslav Klose scored 16 goals across four World Cups for Germany."),
    ("Who holds the world record in the 100-meter sprint?", "Usain Bolt", "athlete", "Usain Bolt", "Usain Bolt set the world record of 9.58 seconds in 2009."),
    ("Which boxer was known as 'The Greatest'?", "Muhammad Ali", "athlete", "Muhammad Ali", "Muhammad Ali was a three-time heavyweight champion and Olympic gold medalist."),
    ("Who has won the most Formula 1 World Championships?", "Lewis Hamilton", "athlete", "Lewis Hamilton", "Lewis Hamilton and Michael Schumacher both have 7 World Championships."),
    ("Which golfer has won the most major championships?", "Jack Nicklaus", "athlete", "Jack Nicklaus", "Jack Nicklaus won 18 major championships during his career."),
    ("Who is the all-time leading scorer in NBA history?", "LeBron James", "athlete", "LeBron James", "LeBron James surpassed Kareem Abdul-Jabbar's scoring record in 2023."),
    ("Which swimmer is known as the 'Flying Fish'?", "Michael Phelps", "athlete", "Michael Phelps", "Michael Phelps earned this nickname due to his incredible swimming speed."),
    
    # Countries (25 pairs)
    ("What is the largest country in the world by land area?", "Russia", "country", "Russia", "Russia covers over 17 million square kilometers."),
    ("Which country has the most time zones?", "France", "country", "France", "France has 12 time zones due to its overseas territories."),
    ("What is the most populous country in the world?", "China", "country", "China", "China has over 1.4 billion people."),
    ("Which country is known as the Land of the Rising Sun?", "Japan", "country", "Japan", "Japan is called this because it's located east of Asia where the sun rises."),
    ("What is the smallest country in the world?", "Vatican City", "country", "Vatican City", "Vatican City covers only 0.17 square miles."),
    ("Which country has the longest coastline?", "Canada", "country", "Canada", "Canada has over 202,000 kilometers of coastline."),
    ("What country is home to Machu Picchu?", "Peru", "country", "Peru", "Machu Picchu is an ancient Incan city located in Peru."),
    ("Which country invented pizza?", "Italy", "country", "Italy", "Pizza originated in Naples, Italy in the 18th century."),
    ("What is the only country that is also a continent?", "Australia", "country", "Australia", "Australia is both a country and a continent."),
    ("Which country has the most natural lakes?", "Canada", "country", "Canada", "Canada has over 2 million lakes."),
    
    # Cities (25 pairs)
    ("What is the capital of Australia?", "Canberra", "city", "Canberra", "Canberra is the capital city of Australia, not Sydney or Melbourne."),
    ("Which city is known as the Big Apple?", "New York City", "city", "New York City", "New York City earned this nickname in the 1920s."),
    ("What is the most populous city in the world?", "Tokyo", "city", "Tokyo", "Greater Tokyo has over 37 million people."),
    ("Which city is home to the Eiffel Tower?", "Paris", "city", "Paris", "The Eiffel Tower was built in Paris for the 1889 World's Fair."),
    ("What city is known as the Eternal City?", "Rome", "city", "Rome", "Rome is called the Eternal City due to its ancient history."),
    ("Which city hosted the 2016 Summer Olympics?", "Rio de Janeiro", "city", "Rio de Janeiro", "Rio de Janeiro, Brazil hosted the 2016 Olympics."),
    ("What is the capital of Canada?", "Ottawa", "city", "Ottawa", "Ottawa is the capital city of Canada."),
    ("Which city is famous for its canals and gondolas?", "Venice", "city", "Venice", "Venice, Italy is built on a lagoon and famous for its waterways."),
    ("What city is home to the Hollywood sign?", "Los Angeles", "city", "Los Angeles", "The Hollywood sign is located in Los Angeles, California."),
    ("Which city is known as the Pearl of the Orient?", "Hong Kong", "city", "Hong Kong", "Hong Kong earned this nickname due to its beauty and prosperity."),
    
    # Historical Figures (25 pairs)
    ("Who painted the ceiling of the Sistine Chapel?", "Michelangelo", "historicalfigure", "Michelangelo", "Michelangelo painted the Sistine Chapel ceiling between 1508 and 1512."),
    ("Which scientist developed the theory of relativity?", "Albert Einstein", "historicalfigure", "Albert Einstein", "Einstein published his theory of relativity in the early 20th century."),
    ("Who wrote 'Romeo and Juliet'?", "William Shakespeare", "historicalfigure", "William Shakespeare", "Shakespeare wrote this famous tragedy around 1595."),
    ("Which explorer is credited with discovering America?", "Christopher Columbus", "historicalfigure", "Christopher Columbus", "Columbus reached the Americas in 1492."),
    ("Who was the first person to walk on the moon?", "Neil Armstrong", "historicalfigure", "Neil Armstrong", "Armstrong stepped on the moon on July 20, 1969."),
    ("Which inventor created the light bulb?", "Thomas Edison", "historicalfigure", "Thomas Edison", "Edison developed the first practical incandescent light bulb."),
    ("Who composed 'The Four Seasons'?", "Antonio Vivaldi", "historicalfigure", "Antonio Vivaldi", "Vivaldi composed this famous set of violin concertos around 1720."),
    ("Which nurse is known as the Lady with the Lamp?", "Florence Nightingale", "historicalfigure", "Florence Nightingale", "Nightingale revolutionized nursing during the Crimean War."),
    ("Who founded Microsoft?", "Bill Gates", "historicalfigure", "Bill Gates", "Bill Gates co-founded Microsoft with Paul Allen in 1975."),
    ("Which civil rights leader gave the 'I Have a Dream' speech?", "Martin Luther King Jr.", "historicalfigure", "Martin Luther King Jr.", "MLK delivered this speech during the 1963 March on Washington."),
    
    # Science (25 pairs)
    ("What is the chemical symbol for gold?", "Au", "scientificterm", "Gold", "Au comes from the Latin word 'aurum' meaning gold."),
    ("How many bones are in the adult human body?", "206", "scientificterm", "Human skeleton", "Adults have 206 bones, while babies are born with about 270."),
    ("What is the speed of light?", "299,792,458 meters per second", "scientificterm", "Speed of light", "This is the speed of light in a vacuum."),
    ("Which planet is closest to the Sun?", "Mercury", "scientificterm", "Mercury", "Mercury is the innermost planet in our solar system."),
    ("What is the largest organ in the human body?", "Skin", "scientificterm", "Human skin", "The skin is the body's largest organ by surface area."),
    ("How many chambers does a human heart have?", "Four", "scientificterm", "Human heart", "The heart has two atria and two ventricles."),
    ("What gas makes up about 78% of Earth's atmosphere?", "Nitrogen", "scientificterm", "Earth's atmosphere", "Nitrogen makes up about 78% of the air we breathe."),
    ("What is the hardest natural substance?", "Diamond", "scientificterm", "Diamond", "Diamond rates 10 on the Mohs hardness scale."),
    ("How many chromosomes do humans have?", "46", "scientificterm", "Human chromosomes", "Humans have 23 pairs of chromosomes, totaling 46."),
    ("What is the smallest unit of matter?", "Atom", "scientificterm", "Atom", "Atoms are the basic building blocks of all matter."),
    
    # Entertainment (25 pairs)
    ("Who directed the movie 'Jaws'?", "Steven Spielberg", "movieorTVseries", "Jaws", "Spielberg directed this 1975 thriller about a great white shark."),
    ("Which movie features the song 'My Heart Will Go On'?", "Titanic", "movieorTVseries", "Titanic", "Celine Dion performed this song for the 1997 film."),
    ("Who played Harry Potter in the film series?", "Daniel Radcliffe", "actororactress", "Daniel Radcliffe", "Radcliffe starred in all eight Harry Potter films."),
    ("Which TV show features characters named Ross, Rachel, and Monica?", "Friends", "movieorTVseries", "Friends", "Friends aired from 1994 to 2004 and remains popular today."),
    ("Who wrote the 'Lord of the Rings' trilogy?", "J.R.R. Tolkien", "writer", "J.R.R. Tolkien", "Tolkien published these fantasy novels in the 1950s."),
    ("Which singer is known as the 'King of Pop'?", "Michael Jackson", "singer", "Michael Jackson", "Jackson earned this title through his incredible success and influence."),
    ("What is the highest-grossing film of all time?", "Avatar", "movieorTVseries", "Avatar", "James Cameron's Avatar earned over $2.9 billion worldwide."),
    ("Who composed 'The Magic Flute'?", "Wolfgang Amadeus Mozart", "composer", "Wolfgang Amadeus Mozart", "Mozart composed this opera in 1791, shortly before his death."),
    ("Which book begins with 'It was the best of times, it was the worst of times'?", "A Tale of Two Cities", "book", "A Tale of Two Cities", "This Charles Dickens novel was published in 1859."),
    ("Who painted 'The Starry Night'?", "Vincent van Gogh", "painter", "Vincent van Gogh", "Van Gogh painted this masterpiece in 1889."),
    
    # Geography (25 pairs)
    ("What is the longest river in the world?", "Nile River", "touristattraction", "Nile River", "The Nile River flows for about 6,650 kilometers through Africa."),
    ("Which mountain range contains Mount Everest?", "Himalayas", "touristattraction", "Himalayas", "Mount Everest is located in the Himalayan mountain range."),
    ("What is the deepest ocean trench?", "Mariana Trench", "touristattraction", "Mariana Trench", "The Mariana Trench reaches depths of over 11,000 meters."),
    ("Which desert is the largest in the world?", "Sahara Desert", "touristattraction", "Sahara Desert", "The Sahara covers about 9 million square kilometers in Africa."),
    ("What is the tallest waterfall in the world?", "Angel Falls", "touristattraction", "Angel Falls", "Angel Falls in Venezuela drops 979 meters."),
    ("Which lake is the largest by surface area?", "Caspian Sea", "touristattraction", "Caspian Sea", "Despite its name, the Caspian Sea is actually a lake."),
    ("What is the southernmost continent?", "Antarctica", "touristattraction", "Antarctica", "Antarctica surrounds the South Pole and is covered in ice."),
    ("Which strait separates Europe and Africa?", "Strait of Gibraltar", "touristattraction", "Strait of Gibraltar", "This strait is only about 14 kilometers wide at its narrowest point."),
    ("What is the largest island in the world?", "Greenland", "touristattraction", "Greenland", "Greenland covers over 2 million square kilometers."),
    ("Which volcano destroyed Pompeii?", "Mount Vesuvius", "touristattraction", "Mount Vesuvius", "Vesuvius erupted in 79 AD, burying the city of Pompeii."),
    
    # Technology (25 pairs)
    ("Who founded Apple Inc.?", "Steve Jobs", "company", "Apple Inc.", "Steve Jobs co-founded Apple with Steve Wozniak in 1976."),
    ("What does 'WWW' stand for?", "World Wide Web", "invention", "World Wide Web", "The World Wide Web was invented by Tim Berners-Lee in 1989."),
    ("Which company created the iPhone?", "Apple", "company", "Apple", "Apple released the first iPhone in 2007."),
    ("What does 'GPS' stand for?", "Global Positioning System", "invention", "GPS", "GPS uses satellites to provide location information."),
    ("Who invented the telephone?", "Alexander Graham Bell", "invention", "Telephone", "Bell received the first patent for the telephone in 1876."),
    ("Which search engine was founded by Larry Page and Sergey Brin?", "Google", "company", "Google", "Google was founded in 1998 while they were PhD students at Stanford."),
    ("What does 'AI' stand for in technology?", "Artificial Intelligence", "invention", "Artificial Intelligence", "AI refers to machines that can perform tasks requiring human intelligence."),
    ("Which social media platform was founded by Mark Zuckerberg?", "Facebook", "company", "Facebook", "Facebook was founded in 2004, initially for college students."),
    ("What does 'USB' stand for?", "Universal Serial Bus", "invention", "USB", "USB is a standard for connecting devices to computers."),
    ("Which company developed the Windows operating system?", "Microsoft", "company", "Microsoft", "Microsoft released the first version of Windows in 1985."),
    
    # Animals (25 pairs)
    ("What is the largest mammal in the world?", "Blue whale", "animal", "Blue whale", "Blue whales can grow up to 30 meters long and weigh 200 tons."),
    ("Which animal is known as the 'King of the Jungle'?", "Lion", "animal", "Lion", "Lions are apex predators known for their strength and majesty."),
    ("What is the fastest land animal?", "Cheetah", "animal", "Cheetah", "Cheetahs can reach speeds of up to 120 km/h."),
    ("Which bird cannot fly but is an excellent swimmer?", "Penguin", "animal", "Penguin", "Penguins have adapted to life in the water rather than flight."),
    ("What is the largest bird in the world?", "Ostrich", "animal", "Ostrich", "Ostriches can grow up to 2.7 meters tall and weigh 150 kg."),
    ("Which animal has the longest neck?", "Giraffe", "animal", "Giraffe", "A giraffe's neck can be up to 2 meters long."),
    ("What is the most venomous snake in the world?", "Inland taipan", "animal", "Inland taipan", "The inland taipan's venom is the most toxic of any snake."),
    ("Which animal is known for its black and white stripes?", "Zebra", "animal", "Zebra", "Each zebra has a unique pattern of stripes."),
    ("What is the largest cat species?", "Tiger", "animal", "Tiger", "Tigers are the largest wild cats, with males weighing up to 300 kg."),
    ("Which animal is known for its ability to change colors?", "Chameleon", "animal", "Chameleon", "Chameleons change color for communication and temperature regulation."),
    
    # Food (30 pairs)
    ("Which spice is derived from the Crocus flower?", "Saffron", "food", "Saffron", "Saffron is one of the world's most expensive spices by weight."),
    ("What is the main ingredient in guacamole?", "Avocado", "food", "Avocado", "Guacamole is a Mexican dip made primarily from mashed avocados."),
    ("Which country is famous for inventing sushi?", "Japan", "food", "Sushi", "Sushi originated in Japan as a method of preserving fish."),
    ("What type of pastry is used to make profiteroles?", "Choux pastry", "food", "Choux pastry", "Choux pastry is a light pastry dough used for various desserts."),
    ("Which fruit is known as the 'king of fruits'?", "Durian", "food", "Durian", "Durian is prized in Southeast Asia despite its strong odor."),
    ("What is the main ingredient in hummus?", "Chickpeas", "food", "Chickpeas", "Hummus is a Middle Eastern dip made from mashed chickpeas."),
    ("Which cheese is traditionally used on pizza?", "Mozzarella", "food", "Mozzarella", "Mozzarella melts well and has a mild flavor perfect for pizza."),
    ("What is the hottest part of a chili pepper?", "Seeds and ribs", "food", "Chili pepper", "The capsaicin that makes peppers hot is concentrated in these areas."),
    ("Which grain is used to make risotto?", "Arborio rice", "food", "Arborio rice", "Arborio rice has high starch content that creates risotto's creamy texture."),
    ("What is the main flavoring in Earl Grey tea?", "Bergamot", "food", "Bergamot", "Bergamot oil gives Earl Grey its distinctive citrusy flavor."),
    ("Which vegetable is the main ingredient in baba ganoush?", "Eggplant", "food", "Eggplant", "Baba ganoush is a Middle Eastern dip made from roasted eggplant."),
    ("What type of wine is Champagne?", "Sparkling wine", "food", "Champagne", "Champagne is a sparkling wine from the Champagne region of France."),
    ("Which nut is used to make marzipan?", "Almond", "food", "Almond", "Marzipan is a confection made primarily from ground almonds and sugar."),
    ("What is the main ingredient in traditional Greek tzatziki?", "Yogurt", "food", "Tzatziki", "Tzatziki is made with yogurt, cucumber, garlic, and herbs."),
    ("Which spice gives curry its yellow color?", "Turmeric", "food", "Turmeric", "Turmeric is responsible for the characteristic yellow color in many curries."),
    ("What type of meat is traditionally used in Peking duck?", "Duck", "food", "Peking duck", "Peking duck is a famous Chinese dish featuring roasted duck."),
    ("Which herb is the main ingredient in pesto?", "Basil", "food", "Basil", "Traditional pesto is made with fresh basil, garlic, pine nuts, and olive oil."),
    ("What is the main alcohol in a Mojito cocktail?", "Rum", "food", "Mojito", "A Mojito is made with white rum, lime juice, mint, and soda water."),
    ("Which bean is used to make traditional Japanese miso soup?", "Soybean", "food", "Miso", "Miso is a fermented soybean paste used in Japanese cuisine."),
    ("What type of pastry is used for eclairs?", "Choux pastry", "food", "Eclair", "Eclairs are made with choux pastry and filled with cream."),

    # Music (25 pairs)
    ("Who composed 'The Four Seasons'?", "Antonio Vivaldi", "composer", "Antonio Vivaldi", "Vivaldi composed this famous set of violin concertos around 1720."),
    ("Which instrument did Mozart primarily play?", "Piano", "composer", "Wolfgang Amadeus Mozart", "Mozart was a virtuoso pianist and composer."),
    ("Who wrote 'Bohemian Rhapsody'?", "Freddie Mercury", "singer", "Queen", "Freddie Mercury wrote this iconic song for the band Queen."),
    ("Which composer wrote 'The Moonlight Sonata'?", "Ludwig van Beethoven", "composer", "Ludwig van Beethoven", "Beethoven composed this famous piano sonata in 1801."),
    ("Who is known as the 'King of Rock and Roll'?", "Elvis Presley", "singer", "Elvis Presley", "Elvis Presley earned this title for his influence on rock music."),
    ("Which band released the album 'Abbey Road'?", "The Beatles", "singer", "The Beatles", "Abbey Road was The Beatles' penultimate studio album."),
    ("Who composed 'The Blue Danube'?", "Johann Strauss II", "composer", "Johann Strauss II", "This famous waltz was composed in 1866."),
    ("Which singer is known as 'The Voice'?", "Frank Sinatra", "singer", "Frank Sinatra", "Sinatra earned this nickname for his distinctive vocal style."),
    ("Who wrote the opera 'Carmen'?", "Georges Bizet", "composer", "Georges Bizet", "Carmen is one of the most popular operas ever written."),
    ("Which instrument is Yo-Yo Ma famous for playing?", "Cello", "musician", "Yo-Yo Ma", "Yo-Yo Ma is one of the world's most renowned cellists."),
    ("Who composed 'Für Elise'?", "Ludwig van Beethoven", "composer", "Ludwig van Beethoven", "This popular piano piece was composed around 1810."),
    ("Which band sang 'Stairway to Heaven'?", "Led Zeppelin", "singer", "Led Zeppelin", "This is considered one of the greatest rock songs of all time."),
    ("Who is known as the 'Queen of Soul'?", "Aretha Franklin", "singer", "Aretha Franklin", "Franklin earned this title for her powerful voice and influence."),
    ("Which composer wrote 'The Nutcracker'?", "Pyotr Ilyich Tchaikovsky", "composer", "Tchaikovsky", "The Nutcracker is a famous ballet composed in 1892."),
    ("Who sang 'My Way'?", "Frank Sinatra", "singer", "Frank Sinatra", "This became one of Sinatra's signature songs."),
    ("Which instrument did Jimi Hendrix play?", "Guitar", "musician", "Jimi Hendrix", "Hendrix was considered one of the greatest guitarists of all time."),
    ("Who composed 'The Marriage of Figaro'?", "Wolfgang Amadeus Mozart", "composer", "Mozart", "This opera was composed in 1786."),
    ("Which singer is known as 'The Material Girl'?", "Madonna", "singer", "Madonna", "Madonna earned this nickname from her hit song and lifestyle."),
    ("Who wrote 'Yesterday' by The Beatles?", "Paul McCartney", "singer", "Paul McCartney", "McCartney wrote this ballad, one of the most covered songs ever."),
    ("Which composer wrote 'Rhapsody in Blue'?", "George Gershwin", "composer", "George Gershwin", "This jazz-influenced classical piece was composed in 1924."),
    ("Who is known as the 'Godfather of Soul'?", "James Brown", "singer", "James Brown", "Brown earned this title for his influence on soul and funk music."),
    ("Which instrument did Louis Armstrong play?", "Trumpet", "musician", "Louis Armstrong", "Armstrong was a legendary jazz trumpeter and singer."),
    ("Who composed 'Swan Lake'?", "Pyotr Ilyich Tchaikovsky", "composer", "Tchaikovsky", "Swan Lake is one of the most famous ballets ever composed."),
    ("Which band released 'Hotel California'?", "Eagles", "singer", "Eagles", "This song became one of the most iconic rock songs of the 1970s."),
    ("Who is known as the 'Piano Man'?", "Billy Joel", "singer", "Billy Joel", "Joel earned this nickname from his hit song 'Piano Man'."),

    # Sports (25 pairs)
    ("Which sport is played at Wimbledon?", "Tennis", "sport", "Tennis", "Wimbledon is the oldest tennis tournament in the world."),
    ("How many players are on a basketball team on the court?", "Five", "sport", "Basketball", "Each team has five players on the court at any time."),
    ("Which country hosted the 2016 Summer Olympics?", "Brazil", "sport", "Olympics", "The 2016 Olympics were held in Rio de Janeiro, Brazil."),
    ("What is the maximum score possible in ten-pin bowling?", "300", "sport", "Bowling", "A perfect game consists of 12 strikes for a score of 300."),
    ("Which sport uses a puck?", "Hockey", "sport", "Hockey", "Ice hockey is played with a rubber puck instead of a ball."),
    ("How many holes are there in a standard golf course?", "18", "sport", "Golf", "A standard round of golf consists of 18 holes."),
    ("Which sport is known as 'the beautiful game'?", "Soccer", "sport", "Soccer", "Soccer is often called the beautiful game due to its artistry."),
    ("What is the highest possible hand in poker?", "Royal flush", "sport", "Poker", "A royal flush consists of A, K, Q, J, 10 all of the same suit."),
    ("Which sport uses terms like 'love' and 'deuce'?", "Tennis", "sport", "Tennis", "These are scoring terms unique to tennis."),
    ("How many minutes are in a soccer match?", "90", "sport", "Soccer", "A soccer match consists of two 45-minute halves."),
    ("Which sport is played on the largest field?", "Polo", "sport", "Polo", "A polo field is the largest in organized sport."),
    ("What is the term for a score of one under par in golf?", "Birdie", "sport", "Golf", "A birdie is one stroke under par for a hole."),
    ("Which sport uses a net that is 6 feet high?", "Volleyball", "sport", "Volleyball", "The volleyball net is set at 6 feet for women's play."),
    ("How many bases are there in baseball?", "Four", "sport", "Baseball", "Baseball has four bases: first, second, third, and home."),
    ("Which sport is Tiger Woods famous for?", "Golf", "sport", "Golf", "Tiger Woods is one of the greatest golfers of all time."),
    ("What is the term for three strikes in a row in bowling?", "Turkey", "sport", "Bowling", "Three consecutive strikes is called a turkey."),
    ("Which sport uses a shuttlecock?", "Badminton", "sport", "Badminton", "Badminton is played with a shuttlecock instead of a ball."),
    ("How many points is a touchdown worth in American football?", "Six", "sport", "American Football", "A touchdown is worth 6 points, with an extra point attempt."),
    ("Which sport is played on ice with stones?", "Curling", "sport", "Curling", "Curling involves sliding stones on ice toward a target."),
    ("What is the term for a perfect serve in tennis?", "Ace", "sport", "Tennis", "An ace is a serve that the opponent cannot touch."),
    ("Which sport uses terms like 'slam dunk'?", "Basketball", "sport", "Basketball", "A slam dunk is when a player forcefully puts the ball through the hoop."),
    ("How many periods are in an ice hockey game?", "Three", "sport", "Ice Hockey", "Hockey games consist of three 20-minute periods."),
    ("Which sport is Serena Williams famous for?", "Tennis", "sport", "Tennis", "Serena Williams is one of the greatest tennis players ever."),
    ("What is the term for hitting the ball over the fence in baseball?", "Home run", "sport", "Baseball", "A home run allows the batter to circle all bases."),
    ("Which sport uses a pommel horse?", "Gymnastics", "sport", "Gymnastics", "The pommel horse is an apparatus used in men's gymnastics."),

    # Movies and TV (25 pairs)
    ("Who directed the movie 'Titanic'?", "James Cameron", "movieorTVseries", "Titanic", "Cameron directed this epic romance film released in 1997."),
    ("Which movie features the line 'May the Force be with you'?", "Star Wars", "movieorTVseries", "Star Wars", "This iconic line is from the Star Wars franchise."),
    ("Who played the character Jack Sparrow?", "Johnny Depp", "actororactress", "Johnny Depp", "Depp portrayed this pirate character in Pirates of the Caribbean."),
    ("Which TV show features characters named Walter White and Jesse Pinkman?", "Breaking Bad", "movieorTVseries", "Breaking Bad", "This crime drama aired from 2008 to 2013."),
    ("Who directed the movie 'Pulp Fiction'?", "Quentin Tarantino", "movieorTVseries", "Pulp Fiction", "Tarantino wrote and directed this 1994 crime film."),
    ("Which actress played Hermione Granger in Harry Potter?", "Emma Watson", "actororactress", "Emma Watson", "Watson played this character throughout the Harry Potter series."),
    ("What is the highest-grossing animated movie of all time?", "Frozen II", "movieorTVseries", "Frozen II", "This Disney sequel earned over $1.4 billion worldwide."),
    ("Who played the Joker in 'The Dark Knight'?", "Heath Ledger", "actororactress", "Heath Ledger", "Ledger's performance earned him a posthumous Oscar."),
    ("Which TV show is set in the fictional town of Hawkins?", "Stranger Things", "movieorTVseries", "Stranger Things", "This Netflix series is set in 1980s Indiana."),
    ("Who directed the movie 'Inception'?", "Christopher Nolan", "movieorTVseries", "Inception", "Nolan wrote and directed this 2010 sci-fi thriller."),
    ("Which actress won an Oscar for 'La La Land'?", "Emma Stone", "actororactress", "Emma Stone", "Stone won Best Actress for her role as Mia."),
    ("What is the name of the coffee shop in 'Friends'?", "Central Perk", "movieorTVseries", "Friends", "Central Perk was the main hangout spot for the characters."),
    ("Who played Iron Man in the Marvel movies?", "Robert Downey Jr.", "actororactress", "Robert Downey Jr.", "Downey Jr. portrayed Tony Stark/Iron Man for over a decade."),
    ("Which movie won the Oscar for Best Picture in 2020?", "Parasite", "movieorTVseries", "Parasite", "This Korean film made history as the first non-English Best Picture winner."),
    ("Who created the TV series 'Game of Thrones'?", "David Benioff and D.B. Weiss", "movieorTVseries", "Game of Thrones", "They adapted George R.R. Martin's novels for television."),
    ("Which actor played Forrest Gump?", "Tom Hanks", "actororactress", "Tom Hanks", "Hanks won an Oscar for this iconic role."),
    ("What is the name of the school in 'Harry Potter'?", "Hogwarts", "movieorTVseries", "Harry Potter", "Hogwarts School of Witchcraft and Wizardry is the magical school."),
    ("Who directed 'The Godfather'?", "Francis Ford Coppola", "movieorTVseries", "The Godfather", "Coppola directed this classic crime saga."),
    ("Which TV show features a character named Tyrion Lannister?", "Game of Thrones", "movieorTVseries", "Game of Thrones", "Tyrion is one of the main characters in this fantasy series."),
    ("Who played the character Neo in 'The Matrix'?", "Keanu Reeves", "actororactress", "Keanu Reeves", "Reeves starred as the protagonist in this sci-fi trilogy."),
    ("Which animated movie features the song 'Let It Go'?", "Frozen", "movieorTVseries", "Frozen", "This Disney song became a global phenomenon."),
    ("Who directed 'Jurassic Park'?", "Steven Spielberg", "movieorTVseries", "Jurassic Park", "Spielberg brought dinosaurs to life in this 1993 blockbuster."),
    ("Which TV show is about a chemistry teacher turned meth cook?", "Breaking Bad", "movieorTVseries", "Breaking Bad", "Walter White's transformation drives this acclaimed series."),
    ("Who played Captain Jack Sparrow's love interest Elizabeth Swann?", "Keira Knightley", "actororactress", "Keira Knightley", "Knightley played this role in the Pirates of the Caribbean series."),
    ("Which movie features the quote 'I'll be back'?", "The Terminator", "movieorTVseries", "The Terminator", "Arnold Schwarzenegger's character says this iconic line."),

    # Literature (25 pairs)
    ("Who wrote 'Pride and Prejudice'?", "Jane Austen", "writer", "Jane Austen", "Austen published this classic novel in 1813."),
    ("Which book begins with 'Call me Ishmael'?", "Moby Dick", "book", "Moby Dick", "This is the famous opening line of Herman Melville's novel."),
    ("Who created the character Sherlock Holmes?", "Arthur Conan Doyle", "writer", "Arthur Conan Doyle", "Doyle created this famous detective character."),
    ("Which novel features the character Atticus Finch?", "To Kill a Mockingbird", "book", "To Kill a Mockingbird", "Harper Lee's novel explores themes of racial injustice."),
    ("Who wrote '1984'?", "George Orwell", "writer", "George Orwell", "Orwell's dystopian novel was published in 1949."),
    ("Which book series features a boy wizard named Harry Potter?", "Harry Potter", "book", "Harry Potter", "J.K. Rowling created this beloved fantasy series."),
    ("Who wrote 'The Great Gatsby'?", "F. Scott Fitzgerald", "writer", "F. Scott Fitzgerald", "This novel captures the Jazz Age in America."),
    ("Which novel begins with 'It was the best of times, it was the worst of times'?", "A Tale of Two Cities", "book", "A Tale of Two Cities", "This Charles Dickens novel is set during the French Revolution."),
    ("Who wrote 'One Hundred Years of Solitude'?", "Gabriel García Márquez", "writer", "Gabriel García Márquez", "This magical realism masterpiece won the Nobel Prize."),
    ("Which book features the character Jay Gatsby?", "The Great Gatsby", "book", "The Great Gatsby", "Gatsby is the mysterious millionaire in Fitzgerald's novel."),
    ("Who wrote 'The Catcher in the Rye'?", "J.D. Salinger", "writer", "J.D. Salinger", "This coming-of-age novel was published in 1951."),
    ("Which novel features the character Elizabeth Bennet?", "Pride and Prejudice", "book", "Pride and Prejudice", "Elizabeth is the spirited heroine of Austen's novel."),
    ("Who wrote 'Brave New World'?", "Aldous Huxley", "writer", "Aldous Huxley", "This dystopian novel was published in 1932."),
    ("Which book features the character Holden Caulfield?", "The Catcher in the Rye", "book", "The Catcher in the Rye", "Holden is the teenage narrator of Salinger's novel."),
    ("Who wrote 'The Lord of the Flies'?", "William Golding", "writer", "William Golding", "This novel explores human nature through stranded schoolboys."),
    ("Which novel features the character Scout Finch?", "To Kill a Mockingbird", "book", "To Kill a Mockingbird", "Scout is the young narrator of Harper Lee's novel."),
    ("Who wrote 'Fahrenheit 451'?", "Ray Bradbury", "writer", "Ray Bradbury", "This dystopian novel is about book burning in the future."),
    ("Which book features the character Winston Smith?", "1984", "book", "1984", "Winston is the protagonist in Orwell's totalitarian nightmare."),
    ("Who wrote 'The Hobbit'?", "J.R.R. Tolkien", "writer", "J.R.R. Tolkien", "This fantasy novel precedes The Lord of the Rings."),
    ("Which novel features the character Bilbo Baggins?", "The Hobbit", "book", "The Hobbit", "Bilbo is the reluctant hero of Tolkien's adventure."),
    ("Who wrote 'Of Mice and Men'?", "John Steinbeck", "writer", "John Steinbeck", "This novella explores friendship during the Great Depression."),
    ("Which book features the characters George and Lennie?", "Of Mice and Men", "book", "Of Mice and Men", "These migrant workers are the main characters in Steinbeck's story."),
    ("Who wrote 'The Grapes of Wrath'?", "John Steinbeck", "writer", "John Steinbeck", "This novel won the Pulitzer Prize for Fiction in 1940."),
    ("Which novel features the Joad family?", "The Grapes of Wrath", "book", "The Grapes of Wrath", "The Joads are Dust Bowl migrants in Steinbeck's epic."),
    ("Who wrote 'Wuthering Heights'?", "Emily Brontë", "writer", "Emily Brontë", "This Gothic novel was published in 1847."),

    # Space and Astronomy (20 pairs)
    ("Which planet is closest to the Sun?", "Mercury", "scientificterm", "Mercury", "Mercury is the innermost planet in our solar system."),
    ("What is the largest planet in our solar system?", "Jupiter", "scientificterm", "Jupiter", "Jupiter is more massive than all other planets combined."),
    ("Which galaxy contains our solar system?", "Milky Way", "scientificterm", "Milky Way", "Our solar system is located in the Milky Way galaxy."),
    ("What is the name of Earth's natural satellite?", "Moon", "scientificterm", "Moon", "The Moon is Earth's only natural satellite."),
    ("Which planet is known as the Red Planet?", "Mars", "scientificterm", "Mars", "Mars appears red due to iron oxide on its surface."),
    ("What is the hottest planet in our solar system?", "Venus", "scientificterm", "Venus", "Venus has the hottest surface due to its thick atmosphere."),
    ("Which planet has the most moons?", "Saturn", "scientificterm", "Saturn", "Saturn has over 80 known moons."),
    ("What is the name of the first artificial satellite?", "Sputnik 1", "scientificterm", "Sputnik 1", "The Soviet Union launched Sputnik 1 in 1957."),
    ("Which planet is famous for its rings?", "Saturn", "scientificterm", "Saturn", "Saturn's ring system is the most prominent in our solar system."),
    ("What is the closest star to Earth?", "Sun", "scientificterm", "Sun", "The Sun is our nearest star, about 93 million miles away."),
    ("Which planet rotates on its side?", "Uranus", "scientificterm", "Uranus", "Uranus has an unusual axial tilt of about 98 degrees."),
    ("What is the name of the space telescope launched in 1990?", "Hubble", "scientificterm", "Hubble Space Telescope", "Hubble has provided incredible images of deep space."),
    ("Which planet has the shortest day?", "Jupiter", "scientificterm", "Jupiter", "Jupiter rotates once every 9 hours and 56 minutes."),
    ("What is the name of the force that keeps planets in orbit?", "Gravity", "scientificterm", "Gravity", "Gravity is the attractive force between masses."),
    ("Which planet is the smallest in our solar system?", "Mercury", "scientificterm", "Mercury", "Mercury is the smallest planet by both mass and volume."),
    ("What is the name of the boundary around a black hole?", "Event horizon", "scientificterm", "Event horizon", "The event horizon is the point of no return around a black hole."),
    ("Which planet has the longest year?", "Neptune", "scientificterm", "Neptune", "Neptune takes about 165 Earth years to orbit the Sun."),
    ("What is the name of the spacecraft that first landed humans on the Moon?", "Apollo 11", "scientificterm", "Apollo 11", "Apollo 11 achieved the first manned Moon landing in 1969."),
    ("Which planet is known for having the Great Red Spot?", "Jupiter", "scientificterm", "Jupiter", "The Great Red Spot is a giant storm on Jupiter."),
    ("What is the name of the theoretical boundary of our solar system?", "Oort Cloud", "scientificterm", "Oort Cloud", "The Oort Cloud is a spherical shell of icy objects."),

    # Mathematics (20 pairs)
    ("What is the value of pi to two decimal places?", "3.14", "scientificterm", "Pi", "Pi is the ratio of a circle's circumference to its diameter."),
    ("What is the square root of 144?", "12", "scientificterm", "Square root", "12 × 12 = 144, so the square root of 144 is 12."),
    ("What is 2 to the power of 8?", "256", "scientificterm", "Exponents", "2^8 = 2×2×2×2×2×2×2×2 = 256."),
    ("What is the sum of angles in a triangle?", "180 degrees", "scientificterm", "Triangle", "The interior angles of any triangle always sum to 180 degrees."),
    ("What is the formula for the area of a circle?", "πr²", "scientificterm", "Circle area", "The area equals pi times the radius squared."),
    ("What is the next prime number after 7?", "11", "scientificterm", "Prime numbers", "11 is the next prime number after 7."),
    ("What is 15% of 200?", "30", "scientificterm", "Percentage", "15% of 200 = 0.15 × 200 = 30."),
    ("What is the hypotenuse of a right triangle with sides 3 and 4?", "5", "scientificterm", "Pythagorean theorem", "Using a² + b² = c², we get 3² + 4² = 5²."),
    ("What is the factorial of 5?", "120", "scientificterm", "Factorial", "5! = 5 × 4 × 3 × 2 × 1 = 120."),
    ("What is the slope of a horizontal line?", "0", "scientificterm", "Slope", "Horizontal lines have no rise, so the slope is 0."),
    ("What is the area of a rectangle with length 8 and width 5?", "40", "scientificterm", "Rectangle area", "Area = length × width = 8 × 5 = 40."),
    ("What is the circumference of a circle with radius 3?", "6π", "scientificterm", "Circle circumference", "Circumference = 2πr = 2π(3) = 6π."),
    ("What is the greatest common divisor of 12 and 18?", "6", "scientificterm", "GCD", "The largest number that divides both 12 and 18 is 6."),
    ("What is the volume of a cube with side length 4?", "64", "scientificterm", "Cube volume", "Volume = side³ = 4³ = 64."),
    ("What is the median of the numbers 3, 7, 2, 9, 5?", "5", "scientificterm", "Median", "When arranged in order (2,3,5,7,9), the middle value is 5."),
    ("What is 7 × 8?", "56", "scientificterm", "Multiplication", "7 × 8 = 56."),
    ("What is the perimeter of a square with side length 6?", "24", "scientificterm", "Square perimeter", "Perimeter = 4 × side = 4 × 6 = 24."),
    ("What is the absolute value of -15?", "15", "scientificterm", "Absolute value", "The absolute value is the distance from zero, so |-15| = 15."),
    ("What is 100 divided by 4?", "25", "scientificterm", "Division", "100 ÷ 4 = 25."),
    ("What is the mode of the numbers 2, 3, 3, 4, 5?", "3", "scientificterm", "Mode", "The mode is the most frequently occurring value, which is 3."),

    # Inventions and Technology (20 pairs)
    ("Who invented the telephone?", "Alexander Graham Bell", "invention", "Telephone", "Bell received the first patent for the telephone in 1876."),
    ("Who invented the light bulb?", "Thomas Edison", "invention", "Light bulb", "Edison developed the first practical incandescent light bulb."),
    ("Who invented the World Wide Web?", "Tim Berners-Lee", "invention", "World Wide Web", "Berners-Lee created the WWW while working at CERN in 1989."),
    ("Who invented the printing press?", "Johannes Gutenberg", "invention", "Printing press", "Gutenberg's printing press revolutionized the spread of information."),
    ("Who invented the airplane?", "Wright Brothers", "invention", "Airplane", "Orville and Wilbur Wright achieved the first powered flight in 1903."),
    ("Who invented the radio?", "Guglielmo Marconi", "invention", "Radio", "Marconi is credited with developing wireless telegraphy."),
    ("Who invented the television?", "John Logie Baird", "invention", "Television", "Baird demonstrated the first working television in 1926."),
    ("Who invented the computer mouse?", "Douglas Engelbart", "invention", "Computer mouse", "Engelbart invented the mouse in 1964."),
    ("Who invented the steam engine?", "James Watt", "invention", "Steam engine", "Watt improved the steam engine design in the 1760s."),
    ("Who invented the vaccine for polio?", "Jonas Salk", "invention", "Polio vaccine", "Salk developed the first successful polio vaccine in 1955."),
    ("Who invented the phonograph?", "Thomas Edison", "invention", "Phonograph", "Edison invented this sound recording device in 1877."),
    ("Who invented the safety pin?", "Walter Hunt", "invention", "Safety pin", "Hunt invented the safety pin in 1849."),
    ("Who invented the zipper?", "Whitcomb Judson", "invention", "Zipper", "Judson patented the 'clasp locker' in 1893."),
    ("Who invented the microwave oven?", "Percy Spencer", "invention", "Microwave oven", "Spencer discovered microwave cooking while working with radar."),
    ("Who invented the Post-it Note?", "Art Fry", "invention", "Post-it Note", "Fry developed Post-it Notes at 3M in the 1970s."),
    ("Who invented the ballpoint pen?", "László Bíró", "invention", "Ballpoint pen", "Bíró patented the ballpoint pen in 1938."),
    ("Who invented Velcro?", "George de Mestral", "invention", "Velcro", "De Mestral invented Velcro after studying burr seeds."),
    ("Who invented the laser?", "Theodore Maiman", "invention", "Laser", "Maiman built the first working laser in 1960."),
    ("Who invented the transistor?", "John Bardeen, Walter Brattain, and William Shockley", "invention", "Transistor", "These three scientists invented the transistor at Bell Labs."),
    ("Who invented the integrated circuit?", "Jack Kilby", "invention", "Integrated circuit", "Kilby invented the IC in 1958, revolutionizing electronics."),

    # World History (20 pairs)
    ("In which year did World War II end?", "1945", "historicalfigure", "World War II", "World War II ended in 1945 with the surrender of Japan."),
    ("Who was the first person to walk on the moon?", "Neil Armstrong", "historicalfigure", "Neil Armstrong", "Armstrong stepped on the moon on July 20, 1969."),
    ("In which year did the Berlin Wall fall?", "1989", "historicalfigure", "Berlin Wall", "The Berlin Wall fell on November 9, 1989."),
    ("Who was the first President of the United States?", "George Washington", "politician", "George Washington", "Washington served as the first President from 1789 to 1797."),
    ("In which year did the Titanic sink?", "1912", "historicalfigure", "Titanic", "The Titanic sank on April 15, 1912."),
    ("Who painted the Mona Lisa?", "Leonardo da Vinci", "painter", "Leonardo da Vinci", "Da Vinci painted this masterpiece in the early 1500s."),
    ("In which year did Christopher Columbus reach the Americas?", "1492", "historicalfigure", "Christopher Columbus", "Columbus reached the Americas on October 12, 1492."),
    ("Who was the leader of Nazi Germany?", "Adolf Hitler", "politician", "Adolf Hitler", "Hitler led Nazi Germany from 1933 to 1945."),
    ("In which year did the American Civil War begin?", "1861", "historicalfigure", "American Civil War", "The Civil War began with the attack on Fort Sumter."),
    ("Who wrote the Declaration of Independence?", "Thomas Jefferson", "politician", "Thomas Jefferson", "Jefferson was the primary author of this founding document."),
    ("In which year did the French Revolution begin?", "1789", "historicalfigure", "French Revolution", "The French Revolution began with the storming of the Bastille."),
    ("Who was the first woman to win a Nobel Prize?", "Marie Curie", "historicalfigure", "Marie Curie", "Curie won the Nobel Prize in Physics in 1903."),
    ("In which year did India gain independence?", "1947", "historicalfigure", "Indian Independence", "India gained independence from Britain on August 15, 1947."),
    ("Who was the longest-reigning British monarch?", "Queen Elizabeth II", "politician", "Queen Elizabeth II", "Elizabeth II reigned for over 70 years until 2022."),
    ("In which year did the Great Depression begin?", "1929", "historicalfigure", "Great Depression", "The Great Depression began with the stock market crash of 1929."),
    ("Who led the civil rights movement in the United States?", "Martin Luther King Jr.", "historicalfigure", "Martin Luther King Jr.", "King was a key leader in the American civil rights movement."),
    ("In which year did the Soviet Union collapse?", "1991", "historicalfigure", "Soviet Union", "The USSR officially dissolved on December 26, 1991."),
    ("Who was the first female Prime Minister of the United Kingdom?", "Margaret Thatcher", "politician", "Margaret Thatcher", "Thatcher served as PM from 1979 to 1990."),
    ("In which year did Nelson Mandela become President of South Africa?", "1994", "politician", "Nelson Mandela", "Mandela became president after the end of apartheid."),
    ("Who discovered penicillin?", "Alexander Fleming", "historicalfigure", "Alexander Fleming", "Fleming discovered penicillin in 1928, revolutionizing medicine.")
]

def create_sample_dataset():
    """Create a sample dataset with the predefined QA pairs"""
    print("Creating sample dataset with 300 QA pairs...")
    
    # Initialize database and sentence transformer (lightweight model)
    db = DatabaseManager()
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Clear existing data
    db.clear_database()
    
    # Add sample QA pairs
    added_count = 0
    for question, answer, topic, example, explanation in SAMPLE_QA_PAIRS:
        # Generate embedding for the question
        embedding = model.encode([question])[0]
        embedding_bytes = embedding.astype(np.float32).tobytes()
        
        # Create QA pair
        qa_pair = QAPair(
            topic=topic,
            example=example,
            question=question,
            answer=answer,
            explanation=explanation,
            embedding=embedding  # Pass numpy array, not bytes
        )
        
        # Add to database
        db.save_qa_pair(qa_pair)
        added_count += 1
        
        if added_count % 50 == 0:
            print(f"Added {added_count} QA pairs...")
    
    print(f"Successfully created dataset with {added_count} QA pairs!")
    
    # Verify the data
    stats = db.get_dataset_stats()
    print(f"Database stats: {stats}")
    
    return added_count

if __name__ == "__main__":
    create_sample_dataset()
