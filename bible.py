from freebible import read_web
import random
def getRandVerse():
    web = read_web()
    list = ['Gen','Exo','Lev','Num','Deut','Josh','Judg','Rth','1 Sam','2 Sam','1 Kgs','2 Kgs','1 Chron', '2 Chron','Ezra','Neh', 'Esth','Job', 'Pslm', 'Prov', 'Eccles', 'Song', 'Isa', 'Jer', 'Lam', 'Ezek', 'Dan', 'Hos', 'Joel', 'Amos', 'Obad','Jnh','Micah', 'Nah','Hab', 'Zeph', 'Haggai', 'Zech', 'Mal', 'Matt', 'Mrk', 'Luk','John', 'Acts', 'Rom', '1 Cor', '2 Cor', 'Gal', 'Ephes', 'Phil', 'Col', '1 Thess', '2 Thess', '1 Tim', '2 Tim', 'Titus', 'Philem','Hebrews', 'James', '1 Pet', '2 Pet', '1 John', '2 John', '3 John', 'Jude', 'Rev']
    
    b = list[random.randint(0,len(list)-1)]
    x = random.randint(1,len(web[b]))
    y = random.randint(1,len(web[b][x]))
    return str((web[b][x][y]))
