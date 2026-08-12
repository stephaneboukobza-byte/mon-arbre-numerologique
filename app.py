import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import unicodedata
import datetime
import os

# ==========================================
# 0. FONCTION UTILITAIRE DE FORMATAGE (PLACÉE EN HAUT)
# ==========================================

def formater_cle(val):
    if val == 11: return "11/2"
    if val == 22: return "22/4"
    if val == 33: return "33/6"
    return str(val)

# ==========================================
# 1. DICTIONNAIRES INTÉGRAUX (TEXTES DU LIVRE)
# ==========================================

DESC_RACINES = {
    1: "• **TALENTS :** L'autonomie et votre côté énergique. Que vous soyez employé ou à votre compte, la règle absolue est d'être autonome : agir, décider, organiser. C'est vital pour vous. Ce talent donne des aptitudes à diriger, commander, être pionnier. Votre énergie communicative sert à aller de l'avant et montrer le chemin.\n\n• **EXCÈS :** Égoïste, grand individualiste, égotique. Nerveux, impulsif, les mots dépassent votre pensée. Sensation d'être seul contre tous. Autoritaire, dur, intolérant... voire tyrannique.\n\n• **NON-ALIMENTÉ :** Vous subissez votre vie, spectateur. Difficulté à prendre votre vie en main, tendance à procrastiner, impatience. L'énergie non utilisée se traduit par des tensions internes et corporelles.",
    2: "• **TALENTS :** L'accompagnement, côté maman. Fait pour collaborer, assister. Aime donner de l'aide et permettre de faire évoluer une situation. Vous préférez la place de numéro deux. Sens du contact, de l'accueil et de la réceptivité. Travail en binôme idéal.\n\n• **EXCÈS :** Pense que l'autre a plus de valeur. Manque de confiance, doute, influençable, complexé, indécis. Se fait exploiter, se laisse envahir par les émotions (crises de panique).\n\n• **NON-ALIMENTÉ :** S'isole, s'enferme, fuit le contact. Activité solitaire sans accompagnement. Sensation d'être inutile, angoisse, mal-être profond.",
    3: "• **TALENTS :** L'expression, côté créateur. Fait pour s'exprimer (physiquement, verbalement, artistiquement) et créer des interactions. Apporte de la nouveauté. Les métiers d'expression sur le devant de la scène conviennent grâce à votre charisme.\n\n• **EXCÈS :** Immature, puéril, naïf. Capricieux, superficiel, m'as-tu-vu. Joueur au point de se mettre en danger.\n\n• **NON-ALIMENTÉ :** Communique peu, s'isole, non-dits. Tendance à tout commencer sans rien finir, dispersé. Le corps crée un éparpillement malgré vous.",
    4: "• **TALENTS :** La persévérance, côté travailleur. Édifier solidement, avec courage et ténacité. S'appuie sur la méthode, l'organisation, la règle. Besoin de cadre et de sécurité dans l'activité et l'univers personnel.\n\n• **EXCÈS :** Cartésien à l'excès (ne croit que ce qu'il voit). Enfermé dans une prison de peurs. Rigide, routinier, pointilleux, maniaque, obtus et conservateur.\n\n• **NON-ALIMENTÉ :** Manque de sérieux, d'organisation, de stabilité. Insécurité affective ou professionnelle entraînant stress, blocages et tensions intenses.",
    5: "• **TALENTS :** L'adaptation, côté indépendant. Fait pour le mouvement et la variété. Liberté d'action absolue. Esprit vif, besoin de bouger physiquement ou intellectuellement. Audacieux, conquérant et pionnier.\n\n• **EXCÈS :** Impulsif, agit avant de réfléchir. Perte de liberté par la dépendance (alcool, drogues, sexe). Instable, opportuniste, prise de risques inconsidérés.\n\n• **NON-ALIMENTÉ :** Crainte de l'inconnu, peur de bouger. S'enferme dans la routine. Sensation de manquer d'air, éparpillement, velléité, étourderie.",
    6: "• **TALENTS :** Le sens des responsabilités, côté soignant. Apporter des solutions, de l'harmonie. Rendre les ambiances conviviales. Aptitudes pour le soin, le bien-être, la beauté. Doué pour prendre des responsabilités familiales ou sociales.\n\n• **EXCÈS :** Perfectionniste fuyant la critique. Jaloux, envieux. Persuadé d'incarner la perfection et de n'avoir jamais tort.\n\n• **NON-ALIMENTÉ :** Coléreux, belliqueux, provoque le conflit pour maîtriser ce qui échappe. Hésitant, refuse les responsabilités.",
    7: "• **TALENTS :** La cérébralité, côté original. Différent, assume sa singularité. Cerveau très actif, besoin de tout comprendre. Dons pour apprendre, expertiser, transmettre et conseiller. Approche spirituelle de la vie.\n\n• **EXCÈS :** Solitaire, froid, hautain. Complexe de supériorité, prétentieux, marginal. Orgueil exigeant qui fait abandonner par crainte d'échouer.\n\n• **NON-ALIMENTÉ :** Pensée incessante car le cerveau crie famine. Manque de confiance, sentiment d'infériorité. Se sent exclu, rejeté, incompris.",
    8: "• **TALENTS :** La combativité, côté bâtisseur. Grande énergie, architecte de projects. Ambition, sens du pouvoir et de la justice. S'accomplit en se réalisant matériellement ou en guérissant/reconstruisant l'humain.\n\n• **EXCÈS :** Dur, violent, dominateur, exploite les autres. Arriviste, malhonnête, procédurier. S'installe en victime perpétuelle ou comportement sadique.\n\n• **NON-ALIMENTÉ :** Sentiment d'illégitimité, de non-valeur. Frustration, injustice. Colère inconsciente générant de la violence envers soi ou autrui.",
    9: "• **TALENTS :** L'ouverture, côté engagé. Fait pour les métiers à vision large, tournés vers l'humain, l'international ou un public. Idéaliste, rêve d'un monde meilleur. Sensibilité extrême et immense besoin de reconnaissance.\n\n• **EXCÈS :** Extrémiste, fanatique (tout ou rien). Utopiste sans sens concret. Dépendant pour fuir la réalité, sensation de se sacrifier, mythomanie.\n\n• **NON-ALIMENTÉ :** Peur des autres, intolérance. Cœur fermé, submergé par les émotions. Dans la lune, sans réalisme.",
    "11/2": "• **TALENTS :** Intuition pure, superaccompagnant. Fait pour se surpasser, faire évoluer et grandir (les gens, concepts, nations). Travail en binôme. Inspiration profonde tournée vers le bien collectif.\n\n• **EXCÈS :** Trop exigeant, dur face à la faiblesse. Fusionnel, exclusif. Manipulateur usant de son intuition. Se sent invincible, tyrannique.\n\n• **NON-ALIMENTÉ :** Égocentré. Doutes écrasants, dévalorisation massive. Humeur cyclothymique et actions d'autodestruction.",
    "22/4": "• **TALENTS :** Énergie la plus colossale, superbâtisseur. Intuition aiguë du monde. Capacités de construction majeures, obligation de se surpasser pour bâtir à très grande échelle pour la collectivité.\n\n• **EXCÈS :** Méprisant, utilisation de l'énergie pour détruire. Extrême dureté, manipulation, mégalomanie, tyrannie.\n\n• **NON-ALIMENTÉ :** Paralysé et emprisonné dans ses peurs immenses. Sensation de vide absolu. L'énergie refoulée mène à la déprime ou dépression sévère.",
    "33/6": "• **TALENTS :** Super-soignant, guide exceptionnel. Aspirations collectives immenses pour guider, améliorer et pacifier.\n\n• **EXCÈS :** Attitude de gourou, utilisation des tiers pour son besoin de puissance.\n\n• **NON-ALIMENTÉ :** Fuit les responsabilités, totally paralysé par les tensions ou critiques."
}

DESC_TRONC = {
    1: """**Catégorie des leaders et/ou des précurseurs**
— **Description :**
Votre objectif consiste à agir, à décider, à montrer le chemin, en prenant des initiatives pour faire évoluer les gens, les consciences, les idées, en étant le premier à réaliser certaines choses (Mozart, né le 27/01 ; Mark Zuckerberg, né le 14/05 ; James Watson, codécouvreur de la structure ADN, né le 6/04).
Cependant, cette tendance pourrait être plus ou moins perturbée si l’une de vos deux racines est de valeur 2 ; les doutes pourraient alors vous empêcher d’agir.
Ce qui vous anime ? Décider, amener les tiers vers un but, vous individualiser. Vous êtes fait pour entreprendre des actions, adopter une attitude dynamique, prendre les devants, lancer des actions et avancer.
Chaque fois que vous vous positionnez dans une attitude passive ou que vous attendez que les événements décident à votre place, vous jouez contre vous ; prenez conscience de votre capacité à montrer l’exemple, à tenir un rôle de précurseur, de leader.
Vous pouvez exprimer l’énergie 1 en étant votre propre chef, en vous mettant à votre compte (profession libérale, chef d’entreprise, artisan ou commerçant, leader politique ou social), en devenant un pionnier (inventeur d’objets ou de concepts, d’un style musical ou artistique, etc., comme Léonard de Vinci, né le 15/04, Michael Jackson, né le 29/08, ou John Lennon, né le 9/10), en travaillant pour un groupe et en étant responsable d’un projet, d’une équipe ou d’une structure.
Si vous êtes employé, il vous faut une grande autonomie ou être responsable d’une équipe. Travailler sous les ordres d’une personne très autoritaire, vous laissant peu de latitude, est totalement contre-nature pour vous et risque de créer un conflit intérieur profond.
— **Quid de votre vie professionnelle ?**
Avez-vous une activité où il y a peu d’autonomie, pas de leadership, pas de prise de décision, aucune initiative ?
Avez-vous la sensation d’être plus spectateur qu’acteur de votre vie ?
Attendez-vous que les autres ou les événements prennent les décisions à votre place ?
Si vous répondez oui à l’une de ces questions, ne soyez plus étonné de votre mal-être, de votre nervosité, de votre autoritarisme ou du sentiment d’être seul contre tous. Vous êtes à côté de ce qui vous est essentiel. Dès que vous vous autoriserez à prendre des décisions (des petites au début), à vous autonomiser, à agir, ce défaut s’estompera et vous aurez le sentiment de revivre !
Prenez votre courage à deux mains, libérez-vous du regard des autres et commencez à décider pour votre vie, car ce qui compte pour vous est de prendre des initiatives — même si vous vous trompez ! —, car vous allez satisfaire votre vraie nature !
— **Vos défauts majeurs si votre nombre 1 s’exprime en négatif :** vous êtes égocentrique, égoïste, autoritaire, égotiste, nerveux, isolé, seul contre tous.""",

    2: """**Catégorie des accompagnateurs**
— **Description :**
Votre objectif est de travailler en binôme, pour apporter de l’aide, pour accompagner les gens, les projets ou les idées, grâce à votre sens de l’accueil, votre écoute.
Ce qui vous anime est de partager, d’assister, de protéger, de soutenir, de défendre. Votre plaisir est de permettre aux personnes, aux projets, aux structures de grandir, d’évoluer (Maurice Béjart et Pierre de Coubertin, nés un 1/01). Le tronc 2 n’est, a priori, pas leader. Cependant, le fait d’être né le 1/01 ou le 10/10 apporte dans votre vie un fort besoin d’autonomie (1), d’action et de leadership (1) pendant les soixante premières années de votre vie. Cela peut créer des tensions internes, car le 1 est leader alors que le 2 a besoin d’être guidé.
De fait, choisir un métier qui nourrit ces deux vibrations contraires peut représenter un dilemme cornélien… Pour contourner cela, il est nécessaire d’exprimer les énergies 2 et 1, en occupant un poste autonome tout en exerçant un métier d’accompagnant (Christine Lagarde, née le 1/01) et en ayant un second fiable ou un associé sur lequel s’appuyer (métiers sociaux et activités de services, métiers de responsabilité dans l’accompagnement des tiers, des structures, des projets, etc.).
Votre confort résultera soit de la création d’un binôme en qui vous aurez toute confiance, soit du travail en bonne intelligence avec un superviseur.
— **Quid de votre vie professionnelle ?**
Exercez-vous un métier où vous êtes totalement seul, sans aucun contact humain ?
Avez-vous une activité où votre sens de l’accompagnement, votre capacité à aider, à assister, n’est jamais utilisée ?
Si vous répondez oui à l’une de ces deux questions, ne soyez plus étonné de douter autant de vous- même, d’être influençable, d’entretenir le sentiment d’être inutile, voire incapable. Vous êtes à côté de ce qui vous est essentiel.
Pour sortir de cette situation, la solution réside dans le fait d’être deux (1 + 1 = 2) afin de ne pas rester seul avec vos doutes. Acceptez de demander de l’aide à un professionnel (coach, thérapeute), à un ami qui saurait rester neutre et vous gagnerez en confiance. Autre possibilité : apportez de l’aide à quelqu’un. Vous êtes tellement doué pour cela, qu’en le faisant, votre estime de soi se renforcera ! Puis trouvez un métier où vos talents d’assistant, d’accompagnateur vont pouvoir s’exprimer et vous vous sentirez tellement mieux !
— **Vos défauts majeurs si votre nombre 2 s’exprime en négatif :** vous doutez, manquez d’assurance et de confiance en vous, vous êtes indécis, influençable, soumis. Vous vous dévaluez.""",

    3: """**Catégorie des créateurs ou des communicants**
— **Description :**
Votre objectif consiste à créer, à communiquer, à échanger dans des domaines extrêmement variés, à créer du lien et des synergies ou parfois à être sur le devant de la scène. Le but est d’exercer tout type de métier qui vous permette d’être en liaison avec les autres afin d’exprimer ce que vous avez à dire.
Cet objectif peut être plus ou moins perturbé si l’une de vos racines est le nombre 7. Votre besoin de vous isoler pourrait alors empêcher votre communication avec les tiers.
En règle générale, parler une langue étrangère vous est aisé. De plus, vous avez un certain charisme (Barack Obama, né le 4/08), le sens de l’humour, un esprit joyeux ou le côté joueur d’un enfant.
Vous avez une grande capacité de résilience (Gandhi, né le 2/10).
Professionnellement, vous pouvez vous exprimer :
• physiquement (sportif de haut niveau, masseur, artiste, musicien, animateur, kinésithérapeute, artisan, etc.) ;
• en communiquant (métiers en rapport avec les médias, la publicité, la politique, par exemple Jacques Attali, né le 1/11) ;
• verbalement : acteur, artiste, chanteur, commerçant, négociateur, thérapeute, enseignant, écrivain, conférencier (Brad Pitt, né le 18/12, Monica Bellucci née le 30/09) ;
• en créant : dessinateur, créateur de concept, d’entreprise, de produits, d’images, métiers dans la haute technologie, etc. (Louis Pasteur, né le 27/12, Quentin Tarentino, né le 27/03), en travaillant dans le domaine de l’enfance (assistante maternelle, animateur sportif, pédopsychologue, etc.).
Attention ! Exercer une profession isolée de tout contact ou sans exprimer votre créativité n’est pas permise est totalement contre-nature pour vous.
— **Quid de votre vie professionnelle ?**
Êtes-vous dans une bulle qui vous isole des autres ?
Exercez-vous un métier sans créativité physique, manuelle, ou verbale ?
Votre part créative s’exprime-t-elle uniquement de façon exceptionnelle ?
Si vous répondez oui à l’une de ces questions, ne soyez plus étonné de votre tristesse ou de ce vide profond en vous. Vous vous êtes éloigné d’un besoin essentiel. Si vous êtes de nature éparpillée ou superficielle, c’est parce que vos talents créateurs, vos capacités de mise en relation ne s’expriment pas suffisamment. Dès que vous vous autoriserez à créer, à vous exprimer, à travailler dans le domaine de la communication, de l’enfance, du sport, à créer du lien, des idées ou des concepts, ce défaut s’estompera.
Identifiez les domaines dans lesquels vous êtes le plus doué pour vous exprimer et osez vous y investir, car c’est votre vraie nature !
— **Vos défauts majeurs si votre nombre 3 s’exprime en négatif :** vous êtes immature, naïf, éparpillé ou dépensier, superficiel.""",

    4: """**Catégorie des constructeurs, des garants de l’ordre**
— **Description :**
Votre objectif consiste à construire avec courage, persévérance et ténacité. Travailleur-né, vous faites partie de ceux qui édifient solidement pour les autres (Neil Armstrong, né le 5/08). Vous avez une capacité de travail et d’organisation importante (Justin Bieber, né le 1/03, Franklin D. Roosevelt, né le 30/01) et aimez les méthodes, la technique, les processus, l’organisation ou les éléments stables, car cela vous apporte de la sécurité. Votre objectif est le long terme.
Cet élément peut être plus ou moins perturbé si l’une de vos racines est le nombre 5. Vos besoins de nouveauté et d’inconnu sont à l’opposé de votre besoin de sécurité. Nous verrons comment vivre avec cela plus loin dans ce chapitre (dans le paragraphe intitulé « Intégrez les harmonies et les ambivalences »).
Parfois, vous ressentez une certaine lenteur qui accompagne vos réalisations. Acceptez-la, car tout ce qui est construit sans précipitation vous donne des gages de solidité, et cela vous rassure.
Vous pouvez exprimer l’énergie 4 en exerçant tout métier qui vous permet :
• d’exercer de l’ordre (militaire, gendarme, police, expert-comptable, notaire, huissier, ordre religieux, fonctionnaire, etc.) ;
• d’utiliser un outil méthodique ou technique (professeur, horloger, menuisier, charpentier, géomètre, ingénieur, météorologue, technicien, ouvrier, etc.) ;
• de construire (architecte, maçon, ouvrier assembleur, etc.) ;
• d’organiser pour les autres, en les protégeant ou en les sécurisant ;
• de maîtriser un art (maître sportif, maître d’une profession, maître spirituel, etc., par exemple le dalaï-lama, né le 6/07, Marie-Claude Pietragalla, née le 2/02).
Attention ! Être totalement livré à l’inconnu et à l’imprévisible sans savoir où vous allez est totalement contre-nature pour vous.
— **Quid de votre vie professionnelle ?**
Avez-vous un métier sans salaire fixe ou sans filet ni perspectives ?
Travaillez-vous sans sécurité, sans méthode, sans organisation ?
Ressentez-vous une part aléatoire trop importante dans votre activité ?
Si vous répondez oui à l’une de ces questions, ne soyez plus étonné de votre tension intérieure, de votre raideur, de votre boule au ventre. Votre tronc n’est pas alimenté. Osez entrer dans une structure ou signez un partenariat récurrent, formez-vous, apprenez une méthode, obtenez un diplôme ou une certification : en un mot, travaillez avec constance pour dépasser vos peurs et vous rassurer, car vous avez besoin d’un minimum de sécurité pour pouvoir construire et travailler.
Si vous êtes de nature maniaque, rigide, pointilleuse ou peureuse, c’est parce que vos talents de constructeur, votre besoin de cadre et/ou la maîtrise de votre métier sont absents de votre vie. Dès que vous vous sentirez en sécurité affective et/ou professionnelle, ce défaut s’estompera. Apprenez à prioriser vos objectifs, à vous organiser, à vous créer un cadre de travail et vous construirez du solide !
— **Vos défauts majeurs si votre nombre 4 s’exprime en négatif :** vos peurs vous bloquent, vous avez tendance à vous autolimiter, à être pointilleux, rigide, maniaque, voire obsessionnel.""",

    5: """**Catégorie des innovants-précurseurs, des personnes en mouvement**
— **Description :**
Votre objectif consiste à aller sur des chemins nouveaux, des terres inconnues, des idées nouvelles : vous êtes un précurseur. Vous avez de grandes capacités d’adaptation ; votre appétit pour la nouveauté vous pousse à vous intéresser à beaucoup de domaines, ce qui peut vous donner un côté touche-à-tout ou difficile à suivre…
Vous êtes profondément épris d’indépendance, de liberté d’action, vous aimez les changements et la diversité des situations (Mikhaïl Gorbatchev, né le 2/03, grand réformateur, mit un terme à la guerre froide avec les États-Unis et lança un mouvement de libéralisation politique, économique et culturelle en URSS. Le chanteur jamaïcain Jimmy Cliff, né le 1/04, est l’artiste reggae à s’être le plus ouvert à d’autres formes de musique, ce qui lui a valu une notoriété internationale).
Cet élément peut être plus ou moins perturbé si l’une de vos racines est de valeur 4. Votre besoin d’être rassuré pourrait vous empêcher d’avoir de l’audace, de partir à l’aventure.
Vous pouvez exprimer l’énergie 5 par le mouvement :
• intellectuel (chercheur, créateur de nouveaux concepts, journaliste, réformateur, etc., Isaac Newton, né le 4/01) ;
• mental (nouveau penseur, précurseur, écrivain, concepteur d’idées nouvelles, etc.) ;
• physique (déménageur, globe-trotteur, commerçant multicarte, VRP, etc.) ;
• de conquête (homme d’État, guerrier, pionnier, par exemple Napoléon Bonaparte, né le 15/08, Margaret Thatcher, née le 13/10, Winston Churchill, né le 30/11).
• et de manière générale tous les métiers à condition de pouvoir exprimer votre besoin d’aller hors du cadre, en inventant une nouvelle façon de l’aborder, en vous ouvrant à de nouvelles pratiques.
Attention ! Un métier routinier, rébarbatif est totalement contre-nature pour vous. L’ennui est votre pire ennemi. Vous pourriez paraître instable et donner la sensation de ne jamais pouvoir vous fixer dans un travail. Expliquez bien à votre entourage qu’il vous est insupportable d’être dans une activité qui ronronne. Changer de métier devient alors vital pour vous.
— **Quid de votre vie professionnelle ?**
Vous ennuyez-vous dans votre activité ?
Faites-vous un travail à la chaîne ou rébarbatif ?
Refusez-vous le changement ? Avez-vous tendance à vous bloquer dans votre évolution ?
Si vous répondez oui à l’une de ces questions, ne soyez plus étonné de la souffrance que vous ressentez, de l’impression de manquer d’oxygène, de mourir à petit feu… Vous n’alimentez pas l’énergie 5 de votre tronc. Si vous êtes éparpillé ou étourdi, c’est parce que vous avez oublié de bouger mentalement face à un blocage. En cherchant à aller dans tous les sens, votre corps exprime ce besoin de mouvement non nourri ! Dès que vous vous autoriserez à créer du changement, ce défaut s’estompera.
Comprenez que si vous êtes insatisfait de votre situation, il faut provoquer le changement ! Osez modifier votre activité, diversifiez-vous, soyez audacieux : vous êtes le champion de l’adaptabilité ! Votre vraie nature s’exprime en allant sur des chemins nouveaux.
— **Vos défauts majeurs si votre énergie 5 s’exprime en négatif :** vous êtes impulsif, imprudent, inconséquent et velléitaire. Vous faites des excès en tout genre, vous êtes instable.""",

    6: """**Catégorie des soignants, des responsables**
— **Description :**
Votre objectif consiste à apporter de l’harmonie, du bien-être, du soin, à guider les gens ou les structures, à apporter des solutions, à valoriser, à prendre des responsabilités. Les mots qui vous plaisent le plus sont « harmonie » et « amélioration ». Vous aimez à créer un esprit de famille partout où vous allez, une ambiance agréable et homogène. Vous ne supportez pas les conflits.
En règle générale, vous êtes perfectionniste. Quand on critique votre travail, vous pensez qu’on ne vous aime pas ou que ce que vous faites n’est pas harmonieux. C’est pour cette raison que vous cherchez la perfection : vous ne supportez pas la critique.
Vous pouvez exprimer l’énergie 6 en étant un soignant :
• dans le domaine de la santé physique et comportementale (infirmier, médecin, psychologue, tous les thérapeutes en général, coach, etc., par exemple Boris Cyrulnik, né le 26/07) ;
• dans le domaine de l’ambiance (artiste, conciliateur, musicien, peintre, cuisinier, etc., par exemple parmi les artistes Sean Connery, né le 25/08, Céline Dion, née le 30/03, et Frank Sinatra, né le 12/12) ;
• dans tous métiers qui demandent du soin et de l’attention pour apporter de la beauté, du bien-être, de l’amélioration : esthétique, décoration, mode, assurance ; pâtisserie, hôtellerie, écologie, etc. ;
• dans le domaine des mentalités pour les faire évoluer (réalisateur, écrivain et conférencier engagé dans une cause, etc.) ;
• dans les activités ou les postes à responsabilité (responsable d’agence, de famille, d’équipe, des finances, pompier, etc.) qui nécessitent de guider (responsables de club, d’une association, d’une communauté, d’un pays, etc. Par exemple, maire, syndicaliste, politicien, etc.).
Si votre tronc comporte l’énergie 33, ce besoin de guider est amplifié et doit être exprimé en utilisant votre grande énergie et votre intuition en cherchant à apporter à la collectivité. Quelques exemples de guide 33 : le général de Gaulle, né le 22/11, Pelé, né le 23/10. Parfois, certains guides tirent le collectif vers l’horreur : Adolf Hitler, né le 20/04.
Attention ! Si vous travaillez dans une structure dont l’ambiance quotidienne est la dispute, les reproches et les tensions, c’est totalement contre votre nature. Préférez partir, car c’est invivable pour vous.
— **Quid de votre vie professionnelle ?**
Travaillez-vous dans un endroit où l’ambiance de travail est tendue, voire conflictuelle ?
Votre entourage quotidien met-il régulièrement vos défauts ou vos erreurs en évidence ?
Vos talents pour améliorer une situation, apporter du bien-être, de l’harmonie ou guider un collectif sont-ils largement sous-utilisés ?
Si vous répondez oui à l’une de ces questions, ne soyez plus étonné de votre sentiment d’épuisement, de manque de sens, de souffrance, de colère. L’énergie 6 de votre tronc n’est pas alimentée. Osez trouver l’activité qui va vous permettre d’exprimer vos qualités de soignant, de créateur d’harmonie, d’amélioration, de mieux-être et vous allez avoir le sentiment de revivre. Comprenez que votre nature vous incite à rendre le monde plus beau, vous êtes doué pour cela ! Si vous cherchez à soigner tous vos proches, même s’ils ne vous le demandent pas, c’est souvent parce que vous n’exprimez pas suffisamment vos talents dans votre activité quotidienne. Prenez conscience que soigner sa famille est l’exercice le plus difficile qui soit à cause du manque de neutralité (trop d’affectif) et c’est pour cela que cela vous fatigue tant.
— **Vos défauts majeurs si votre nombre 6 s’exprime en négatif :** vous êtes irresponsable, jaloux, indécis, coléreux et envieux, guerrier et rancunier.""",

    7: """**Catégorie de ceux qui réfléchissent, conseillent, sont originaux**
— **Description :**
Votre objectif consiste à réfléchir, à analyser, à observer, à être constamment en recherche. Votre cerveau est tout le temps en activité, en train de penser. Vous avez besoin de comprendre, d’apprendre, de recevoir, pour ensuite analyser, conseiller, devenir expert, transmettre, enseigner.
Vous avez aussi la sensation d’être profondément différent des autres, l’impression d’être un être original, voire un « extraterrestre ». C’est une chance qu’il faut cultiver au lieu de vivre cela comme un handicap. Vous êtes fait pour exprimer cette singularité, la cultiver ; assumez-la (Dalí, né le 11/05 ; Cristiano Ronaldo, né le 5/02, surnommé CR7 et dont le maillot est le 7 !).
Toutes les activités intellectuelles et/ou spirituelles vous sont nécessaires et vous passionnent (René Descartes, né le 31/03 ; Mère Teresa, née le 26/08). Pour ces raisons, vous avez du talent pour vous remettre en question en travaillant sur vous.
Cet élément peut être plus ou moins perturbé si l’une de vos racines est le nombre 8 (matérialiste), car l’aspect matériel (l’avoir) contrarie le 7 (qui aime s’exprimer au niveau de l’être).
Vous pouvez exprimer l’énergie 7 :
• en étant en apprentissage, en formation, en faisant de longues études, en enseignant, en transmettant (professeur, conférencier, écrivain, philosophe, etc.) ;
• en cultivant votre singularité ; en abordant votre métier d’une façon totalement originale, en étant excentrique, voire marginal ;
• en devenant expert dans votre métier (chercheur, consultant, stratège, conseiller, spécialiste, analyste, critique professionnel, etc. ; par exemple Haroun Tazieff, né le 11/05) ;
• en vous tournant vers la spiritualité (sage, religieux, moine, ésotérisme, etc., par exemple Nelson Mandela, né le 18/07) ;
• en travaillant dans le domaine de l’histoire, de la culture, des personnes âgées.
Attention ! Exercer un métier uniquement manuel, sans rien apprendre, sans aucune intervention de votre cerveau est totalement contre-nature pour vous.
— **Quid de votre vie professionnelle ?**
Êtes-vous complexé par votre différence ou avez-vous l’impression d’être incompris ?
Balayez-vous d’un revers de la main toute forme d’apprentissage ou de spiritualité ?
Vous enfermez-vous dans votre caverne en adoptant une attitude passive ?
Mettez-vous la barre très haut (expert), voire trop haut et cela vous « bloque-t-il » ?
Si vous répondez oui à l’une de ces questions, ne soyez plus étonné de votre manque de confiance en soi, de votre déprime (Marilyn Monroe, née le 1/06). Vous n’alimentez pas l’énergie 7 de votre tronc. Le manque de confiance se soigne par de l’apprentissage, par un travail sur soi.
Si vous avez des difficultés pour débrancher votre cerveau sans passer par la télévision, la musique, les psychotropes, la suralimentation, les drogues ou l’alcool pour vous sentir en paix, comprenez que c’est votre cerveau qui vous crie « j’ai faim ! ». Vous ne l’alimentez pas suffisamment. Faites travailler votre cerveau gauche (l’apprentissage, la transmission, la réflexion, l’analyse, etc.), mais aussi et surtout votre cerveau droit. Pour cela, écoutez votre intuition et travaillez sur vous (thérapies, yoga, méditation, etc.). Vous serez ainsi en phase avec votre vraie nature et vous vous sentirez mieux !
— **Vos défauts majeurs si votre nombre 7 s’exprime en négatif :** vous êtes passif (vous pensez trop), froid, égocentrique, isolé, vous avez un sens aigu de la critique (sentiment de supériorité créé paradoxalement par un grand manque de confiance en vous), vous pouvez même être misanthrope.""",

    8: """**Catégorie de ceux qui construisent avec beaucoup d’énergie**
— **Description :**
Le « 8 » est un constructeur. Il peut s’exprimer de deux façons totalement différentes : dans l’avoir (cercle du bas dans le 8) ou dans l’être (cercle du haut dans le 8). Pour certains d’entre vous, l’objectif consiste à réaliser des projets ambitieux, car ils ont une belle puissance de réalisation. Vous aimez le pouvoir, la réussite matérielle, jouir d’une belle situation socioprofessionnelle (Francis Bouygues, né le 5/12 ; Steve Jobs, né le 24/02). Pour d’autres, l’objectif consiste à permettre aux individus, aux projets de se réaliser. Ce sont des soignants au niveau des mentalités, de la conscience : on les appelle les « guérisseurs de l’âme » (par exemple Jacques-Yves Cousteau, né le 11/06).
Certains d’entre vous oscillent entre les deux options.
Quel que soit votre choix, vous ne supportez pas l’injustice, vous êtes un combattant potentiel.
Ce qui vous anime est de construire ou d’emmener les projets, les idées, les tiers vers un but. Vous êtes doté d’une grande énergie qui vous rend infatigable (Pablo Picasso, né le 25/10) et vous donne la capacité à vous relever d’un échec et à aller toujours plus loin avec courage.
Vous pouvez exprimer votre énergie 8 :
• en étant une personne de pouvoir et d’ambition (homme ou femme d’affaires, politicien, sportif de haut niveau : Vladimir Poutine, né le 7/10 ; Alain Prost, né le 24/02 ; Golda Meir, née le 3/05 ; Carl Lewis, né le 1/07) ;
• en construisant pour les autres (architecte, scientifique, concepteur d’idées, de projets, etc., Albert Einstein, né le 14/03, Walt Disney, né le 5/12) ;
• en exerçant une activité en rapport avec la justice (avocat, juge, huissier, magistrat, policier, etc.) ;
• en faisant évoluer les consciences (écologiste, thérapeute ou exercer une activité en travaillant sur la conscience, ainsi que tout métier dédié à l’évolution de la planète, auteur, etc.).
Le point fondamental à comprendre avec l’énergie 8 de votre tronc réside dans le besoin de prendre votre place au niveau professionnel et/ou sociofamilial sans attendre qu’on vous la donne. Si pour cela vous utilisez la violence ou la malhonnêteté, vous vous trompez de combat. Apprenez plutôt à croire en vous et à démontrer votre légitimité, avec tact et calme. Vivre dans un système qui crée de l’injustice est totalement contre-nature pour vous. Attention à ne pas créer de l’injustice vous-même en contrepartie.
— **Quid de votre vie professionnelle ?**
Subissez-vous de la violence, de l’injustice, ou êtes-vous frustré ?
Avez-vous la sensation de ne pas vous réaliser ?
Attendez-vous que les solutions viennent de l’extérieur ?
Si vous répondez oui à l’une de ces questions, ne soyez plus étonné de votre sentiment d’être détruit de l’intérieur, vide. Vous avez une violence intérieure qui vous fait bouillir… Cela indique que l’énergie 8 de votre tronc n’est pas alimentée. Si vous êtes de nature violente (verbalement ou physiquement) envers les tiers ou envers vous-même, si vous ressentez de la frustration, de l’injustice, si vous êtes la victime de quelqu’un, cela indique que vous avez des difficultés à prendre votre place, à vous sentir légitime. Dès que vous vous autoriserez à exprimer votre valeur, à vous respecter et à vous faire respecter, en travaillant sur vous, vous vous sentirez mieux. Osez vous réaliser, croyez en vous, prenez votre place, exprimez votre légitimité avec calme et justesse et vous allez avoir le sentiment de revivre !
— **Vos défauts majeurs si votre énergie 8 s’exprime en négatif :** vous êtes arriviste, votre honnêteté est à géométrie variable, vous êtes violent et dur, injuste et dominateur (Heinrich Himmler, né le 7/10) ou vous avez un côté « je suis victime et je ne fais rien pour sortir de ce statut ».""",

    9: """**Catégorie de ceux qui rassemblent, qui sont portés vers l’international**
— **Description :**
Votre objectif consiste à comprendre la planète au sens large, en parcourant le monde, en cherchant à comprendre la dimension humaine, en étant tourné vers le collectif, ou encore en réalisant une œuvre ou un travail public (Marie Curie, née le 7/11).
Généralement sensible, émotif et bien souvent idéaliste ou tourné vers l’universalité, vous rêvez d’un monde meilleur. Cela vous rend souvent passionné, voire engagé. Vous aimez rassembler.
Vous pouvez exprimer l’énergie 9 :
• en voyageant : toute profession internationale comme sportif de haut niveau (Rafael Nadal, né le 3/06), astronaute (Patrick Baudry, né le 6/03), chanteur, politicien, négociant, diplomate, activités extraterritoriales, etc. ; ou en travaillant avec une structure étrangère ;
• en réalisant des œuvres publiques (artiste, scientifique, leader, architecte, écrivain, etc., par exemple Gustave Eiffel, né le 15/12 ; Léon Tolstoï, né le 9/09) ; ou en ayant une vie publique : artistes, sportifs, acteur, etc. (Josephine Baker, née le 3/06 ; Line Renaud, née le 2/07 ; Pharrel Williams, né le 5/04 ; Harald Schumacher, né le 6/03).
• en vous impliquant dans une démarche de charité ou d’empathie (travail pour une ONG, pour une cause humanitaire, pour la protection de la faune, etc., par exemple Amma, née le 27/09) ;
• en étant dans les médias, en vous passionnant pour une activité médiatisée : télévision, radio, Internet, etc. (Denis Brogniart, animateur de « Koh-Lanta », né le 12/06 ; Nikos Aliagas, animateur de « The Voice », né le 13/05) ;
• dans les métiers permettant la compréhension de l’être humain, du monde (ressources humaines, thérapeute, toutes les sciences de la vie et de la Terre, etc.) ;
• dans les activités « étranges » (ésotérisme, paranormal, le secteur du handicap, OVNI, etc.) ;
• dans les métiers du luxe (ce qui brille) ou du rêve (gastronomie, haute couture, parfum, hôtellerie, parc d’attractions, show-biz, par exemple Yves Saint Laurent, né le 1/08 ; Pierre Cardin, né le 2/07 ; Giorgio Armani né le 11/07).
• et enfin dans les activités publiques (grandes administrations, orateur, politique, etc.).
Attention ! Avoir une activité solitaire, ou sans intérêt collectif, est totalement contre-nature pour vous.
— **Quid de votre vie professionnelle ?**
Vivez-vous dans l’illusion ou le rêve ?
Exercez-vous une activité où l’humain n’a pas sa place ?
Avez-vous le sentiment de ne pas vous intéresser au monde ?
Si vous répondez oui à l’une de ces questions, ne soyez plus étonné de votre nervosité, ou de cet émotionnel qui s’emballe, ou encore de ce sentiment d’inutilité. Vous n’alimentez pas l’énergie 9 de votre tronc. Si vous êtes de nature rêveuse, dans la lune, c’est parce que vous voyagez dans votre tête au lieu de chercher à découvrir le monde et l’être humain. Écoutez votre sensibilité et vos émotions pour vous engager dans la défense d’une cause, d’une idée, d’une communauté ; ou pour comprendre le monde et l’être humain ; ou encore pour exprimer vos talents et les partager avec le plus grand nombre. Vous êtes doué pour cela, c’est votre nature !
— **Vos défauts majeurs si votre énergie 9 s’exprime en négatif :** vous êtes rêveur et peu concret, fanatique, émotif, ce qui vous handicape, vous vivez dans une réalité fantasmée (mythomanie), vous êtes nerveux, dépendant à quelque chose (alcool, drogue, etc.).""",

    "11/2": """**Catégorie des superaccompagnateurs, des inspirés**
— **Description :**
Vous êtes doté d’une grande intuition… à condition que vous l’écoutiez ! Vos puissantes antennes vous permettent de sentir le monde, les gens et les situations avec beaucoup de finesse.
Votre objectif consiste à vous surpasser, car l’énergie que vous avez est un « booster » personnel qui vous permet d’aider et d’accompagner les autres, de faire évoluer et grandir les tiers, les projets, les structures, les situations, voire les nations (Sigmund Freud, né le 6/05 ; Nicolas Sarkozy, né le 28/01 ; François Hollande, né le 12/08).
Ces atouts impliquent toujours des obligations collectives. Si vous utilisez vos points forts uniquement à des fins égoïstes, vous passerez à côté de votre mission et vivrez des déconvenues. La notion de collectif ne signifie pas qu’il faille obligatoirement vous occuper d’une équipe ; l’idée consiste à vous engager dans une activité qui concerne un nombre varié et multiple de personnes ou d’actions.
Se surpasser signifie dépasser ses doutes et avoir foi en soi, quoi qu’il arrive ! Il est normal que votre humeur connaisse des hauts et des bas : il est difficile d’être tout le temps engagé à fond. Dès que vous n’êtes plus dans le surpassement (énergie 11), vous passez dans l’énergie 2, l’accompagnant. Après une phase de récupération, cherchez à nouveau à vous mettre dans une posture de surpassement pour éviter de ressentir une perte de sens, d’être peu utile.
Le 11, une fois réduit, devient 2 ; cela signifie que vous avez besoin de vivre professionnellement ou personnellement à deux, cela vous rassure et vous apporte une force supplémentaire. Même ceux qui ont l’habitude de décider seuls ont dans leur entourage quelqu’un de très proche sur qui ils peuvent compter (Simone Veil, née le 13/07, mariée à Antoine Veil pendant soixante-huit ans ; Donald Trump, né le 14/06 et son vice-président Mike Pence).
Vous pouvez exprimer l’énergie 11 en exerçant :
• tous les métiers qui nécessitent de l’intuition : chercheur, artiste, créateur, thérapeute, médium, etc. (Bill Gates, né le 28/10 ; Orson Welles, né le 6/05 ; Pierre Curie, né le 15/05) ;
• tous les métiers qui accompagnent ou font évoluer les choses à partir du moment où vous vous surpassez ;
• tous les métiers tournés vers le collectif (Jimmy Carter, né le 1/10).
— **Quid de votre vie professionnelle ?**
Avez-vous la sensation de ne pas accompagner les tiers, de ne pas les aider à évoluer ?
Exercez-vous un métier où vous êtes tout seul, totally livré à vous-même ou sans aucun contact ?
Avez-vous la sensation de régresser, de ne plus avancer, de ne servir à rien ?
Si vous répondez oui à l’une de ces questions, ne soyez plus étonné de douter autant, de penser que vous êtes inutile, incapable : vous n’alimentez pas votre énergie 11.
Si vous avez tendance à vous dévaloriser, si vous êtes de nature autodestructrice (toute action personnelle qui joue contre vous : troubles du comportement alimentaire, troubles du schéma corporel, troubles du comportement social, etc.), cela s’explique : vos doutes sont à la mesure de votre puissance. Quand vous n’utilisez pas vos dons, vous avez la sensation de ne servir à rien. Acceptez de demander de l’aide à un professionnel (coach, thérapeute) ou un ami ou, à l’inverse, apportez de l’aide à quelqu’un : vous êtes tellement doué pour cela, qu’en le faisant, votre estime de soi augmentera ! Travaillez en binôme : en ayant une personne de confiance à vos côtés, en aidant ou en assistant quelqu’un. Dès que vous vous autoriserez à vous engager dans des actions d’accompagnement pour permettre aux autres d’évoluer et de grandir, vous irez mieux !
— **Vos défauts majeurs si votre nombre 11 s’exprime en négatif :** vous êtes tyrannique, manipulateur, avez de nombreux doutes, des capacités d’autodestruction ou d’autodévaluation, car vous n’utilisez pas vos dons (énergie et intuitions) sauf à des fins personnelles.""",

    "22/4": """**Catégorie des superconstructeurs**
— **Description :**
Vous êtes doté d’une immense énergie (la plus forte de tous les nombres !) et d’une grande intuition… à condition que vous l’écoutiez !
Vous ressentez le monde, les gens, les situations, les projets, avec beaucoup d’acuité.
Votre objectif consiste à vous surpasser, car votre énergie est là pour vous permettre de construire pour les autres.
Cet élément peut être plus ou moins perturbé si l’une de vos racines est le nombre 2 ; vos doutes pourraient freiner votre puissance de réalisation.
Ces dons (énergie, intuition, besoin de construire à grande échelle) impliquent des obligations collectives. Si vous utilisez vos points forts uniquement à des fins égoïstes, vous passerez à côté de votre mission et vivrez des déboires. Plus on reçoit, plus on doit donner !
Se surpasser signifie dépasser ses peurs, ses blocages. Dès que vous n’êtes plus dans le surpassement (énergie 22), vous vous trouvez dans l’énergie 4, le travailleur régulier : il est difficile d’être tout le temps au maximum. Après une phase de récupération, cherchez à nouveau à vous mettre dans une posture de surpassement pour éviter d’avoir la sensation d’être sous-employé, de déprimer, voire de ne servir à rien.
Vous pouvez exprimer l’énergie 22 :
• en développant votre puissance de réalisation : tous les métiers qui demandent du courage, du surpassement par rapport à votre milieu d’origine (Leonardo DiCaprio, né le 11/11) ;
• en utilisant votre intuition et/ou votre magnétisme : génie, guérisseur, artiste, créateur (Fédor Dostoïevski, né le 11/11) ;
• en construisant pour la postérité ou pour la collectivité ; tous les métiers qui servent la communauté, qui laissent une œuvre collective (Luciano Pavarotti, né le 12/10 ; René Goscinny, né le 14/08) ;
• en effectuant un métier où vous allez pouvoir transmettre votre énergie à ceux qui n’ont pas la chance d’en avoir autant que vous.
Attention ! Être inactif, au foyer, au chômage est totalement contre-nature pour vous. Cela vous déprime !
— **Quid de votre vie professionnelle ?**
Travaillez-vous pour la communauté ou pour un collectif, êtes-vous dans le surpassement ?
Êtes-vous sans emploi, sans projet ?
Avez-vous la sensation de régresser, de ne plus avancer ?
Avez-vous la sensation de ne pas utiliser votre énergie, de ne servir à rien ?
Si vous répondez oui à l’une de ces questions, ne soyez plus étonné de votre profond mal-être, de votre déprime. L’énergie 22 de votre tronc n’est pas alimentée. Si vous avez tendance à vous bloquer, à vous limiter, ou à vous sentir dépressif, c’est parce que vous avez des peurs ; celles-ci sont à la mesure de votre puissance. Pour les dépasser, travaillez sans relâche, avec méthode et constance ; mettez des priorités dans vos objectifs ; évitez impérativement l’isolement et tournez-vous vers les autres en apprenant à communiquer ce que vous ressentez. Travaillez avec un thérapeute sur vos peurs, vos blessures, votre culpabilité, vos blocages, qui bien souvent n’ont aucun sens, car ils appartiennent au passé… Ainsi, votre énergie personnelle reprendra du poil de la bête ! Enfin, vivez l’instant présent au lieu de vous focaliser sur le résultat ! Dès lors, vos peurs et vos blocages s’estomperont.
— **Vos défauts majeurs si votre énergie 22 s’exprime en négatif :** vos peurs sont de nature bloquante ou paralysante ; vous vous autolimitez ; vous vous servez de votre intuition pour manipuler, vous avez un côté tyrannique (Adolf Eichmann, né un 19/03) ; vous êtes déprimé ou dépressif et dans quelques cas limites atteint de folie."""
}

DESC_TRONC[33] = DESC_TRONC[6]

# --- LES 4 CLÉS STRUCTURÉES (SMILEYS SÉPARÉS) ---

DESC_ECORCE_COMMUNE = {
    1: "😊 **Vos qualités si vous utilisez votre nombre 1 en positif :**\nVous êtes perçu comme autonome, individualiste, indépendant. Volontaire et habile, on remarque votre énergie et votre capacité d'action.\n\n🙁 **Vos défauts si vous exprimez votre nombre 1 en négatif :**\nVous pouvez donner la sensation que tout le monde est contre vous. Vous pouvez être orgueilleux, égoïste, égocentrique ou avoir des difficultés à vous décider.",
    2: "😊 **Vos qualités si vous utilisez votre nombre 2 en positif :**\nVous êtes perçu comme sensible, accueillant et accompagnant. Votre sens de l'écoute facilite la vie à deux.\n\n🙁 **Vos défauts si vous exprimez votre nombre 2 en négatif :**\nVous pouvez douter de vous, être influençable, ou développer une carapace dure et froide face à l'adversité.",
    3: "😊 **Vos qualités si vous utilisez votre nombre 3 en positif :**\nVous êtes perçu comme souriant, communicant, créatif et extraverti. On aime votre charme et votre sociabilité.\n\n🙁 **Vos défauts si vous exprimez votre nombre 3 en négatif :**\nVous pouvez être dispersé, éparpillé, immature, naïf, superficiel ou boudeur.",
    4: "😊 **Vos qualités si vous utilisez votre nombre 4 en positif :**\nVous êtes perçu comme courageux, sérieux, fiable et organisé. On peut compter sur votre droiture.\n\n🙁 **Vos défauts si vous exprimez votre nombre 4 en négatif :**\nVous pouvez être entêté, fermé, cassant, rigide et totalement bloqué par vos peurs.",
    5: "😊 **Vos qualités si vous utilisez votre nombre 5 en positif :**\nApprécié pour votre vivacité, votre audace, votre curiosité et votre grande adaptabilité.\n\n🙁 **Vos défauts si vous exprimez votre nombre 5 en négatif :**\nVous pouvez être instable, impulsif, caméléon, ou dépendant de plaisirs immédiats.",
    6: "😊 **Vos qualités si vous utilisez votre nombre 6 en positif :**\nVous êtes perçu comme attentionné, responsable, axé sur l'harmonie et l'esprit de famille.\n\n🙁 **Vos défauts si vous exprimez votre nombre 6 en négatif :**\nVous fuyez le conflit, ou devenez possessif, jaloux, coléreux ou rancunier.",
    7: "😊 **Vos qualités si vous utilisez votre nombre 7 en positif :**\nVous êtes perçu comme original, observateur, cérébral. Capable de transmettre et de guider.\n\n🙁 **Vos défauts si vous exprimez votre nombre 7 en négatif :**\nVous réfléchissez trop, incapable de décider. Vous paraissez marginal, triste ou hautain.",
    8: "😊 **Vos qualités si vous utilisez votre nombre 8 en positif :**\nVous êtes perçu comme combatif, courageux, productif. Un bâtisseur doté d'un sens aigu de la justice.\n\n🙁 **Vos défauts si vous exprimez votre nombre 8 en négatif :**\nVous pouvez être violent, agressif, injuste, arriviste, ou enfermé dans un rôle de victime.",
    9: "😊 **Vos qualités si vous utilisez votre nombre 9 en positif :**\nVous êtes perçu comme sensible, altruiste, idéaliste et engagé passionnément pour les autres.\n\n🙁 **Vos défauts si vous exprimez votre nombre 9 en négatif :**\nVous pouvez être un utopiste vivant dans l'illusion, émotif à l'excès, cherchant des états parallèles.",
    11: "😊 **Vos qualités si vous utilisez votre nombre 11 en positif :**\nVous êtes perçu comme un superaccompagnant intuitif, électrique, inspiré et visionnaire.\n\n🙁 **Vos défauts si vous exprimez votre nombre 11 en négatif :**\nVous pouvez avoir des humeurs en montagnes russes, risque de dureté ou de dépression si non canalisé.",
    22: "😊 **Vos qualités si vous utilisez votre nombre 22 en positif :**\nVous êtes perçu comme un superbâtisseur ambitieux, un génie créateur pour la communauté.\n\n🙁 **Vos défauts si vous exprimez votre nombre 22 en négatif :**\nVous pouvez paraître enfermé dans un monde étroit, lourd ou dépressif si bloqué par vos peurs."
}

DESC_ECORCE_SPECIFIQUE = {
    1: "• **Spécificité (Né le 1 ou 10) :** Besoin d'être sur le devant de la scène, relation parfois utilitaire aux autres.\n• **Spécificité (Né le 19) :** Grande capacité de rebond mais exigence hautaine face à l'imperfection.\n• **Spécificité (Né le 28) :** Aptitude pour le binôme, matérialité importante et attention à la violence verbale.",
    2: "• **Spécificité (Né le 2 ou 20) :** Facilité pour le couple, la solitude pèse lourdement.\n• **Spécificité (Né le 11 ou 29) :** Superaccompagnant intuitif et électrique, mais humeurs en montagnes russes.",
    3: "• **Spécificité (Né le 3 ou 30) :** Énergie physique, charisme et talents créatifs prononcés.\n• **Spécificité (Né le 12 ou 21) :** Sociabilité chaleureuse, sens de l'observation et équilibre relationnel.",
    4: "• **Spécificité (Né le 4) :** Bâtisseur axé sur la productivité et la sécurité.\n• **Spécificité (Né le 13) :** Oscille entre travail intense et blocages karmiques.\n• **Spécificité (Né le 22) :** Visionnaire ambitieux pour la communauté ou repli anxiogène.\n• **Spécificité (Né le 31) :** Le plus communicant des 4, fort potentiel d'innovation.",
    5: "• **Spécificité (Né le 5 ou 14) :** Esprit d'indépendance farouche, opportuniste ou conquérant.\n• **Spécificité (Né le 23) :** Sens du contact, charme et ouverture d'esprit.",
    6: "• **Spécificité (Né le 6) :** Raffinement, sens esthétique et nature conciliante.\n• **Spécificité (Né le 15) :** Dynamisme redoutable, réactivité face aux opportunités.\n• **Spécificité (Né le 24) :** Discrétion, organisation rigoureuse et sens du service.",
    7: "• **Spécificité (Né le 7) :** Goût prononcé pour le calme et la profondeur intellectuelle.\n• **Spécificité (Né le 16) :** Fierté marquée, exigence et gestion des relations complexes.\n• **Spécificité (Né le 25) :** Écoute fine, empathie et capacité d'adaptation.",
    8: "• **Spécificité (Né le 8) :** Puissance de travail hors norme pour bâtir et durer.\n• **Spécificité (Né le 17) :** Esprit analytique poussé et quête de sens global.\n• **Spécificité (Né le 26) :** Attention portée à la structure et aux proches.",
    9: "• **Spécificité (Né le 9) :** Vagues émotionnelles intenses, envergure internationale.\n• **Spécificité (Né le 18) :** Indépendance marquée, attrait pour le pouvoir ou l'action publique.\n• **Spécificité (Né le 27) :** Cérébralité et volonté de faire évoluer les consciences."
}

DESC_BRANCHES = {
    0: "• **QUALITÉ MANQUANTE :**\nL'action n'est pas votre réflexe premier. Vous devez apprendre à initier.",
    1: "😊 **Vos qualités si vous utilisez votre nombre 1 en positif :**\nVous aimez agir en dirigeant votre vie, en prenant des décisions, en allant de l'avant pour montrer le chemin.\n\n🙁 **Vos défauts si vous exprimez votre nombre 1 en négatif :**\nVous avez des difficultés à agir, tendance à subir ou à attendre que les autres décident.",
    2: "😊 **Vos qualités si vous utilisez votre nombre 2 en positif :**\nVous agissez avec empathie, bienveillance, en binôme, en portant attention à l'autre.\n\n🙁 **Vos défauts si vous exprimez votre nombre 2 en négatif :**\nVous êtes submergé par les doutes, avez le sentiment de ne rien valoir, ou faites preuve de soumission.",
    3: "😊 **Vos qualités si vous utilisez votre nombre 3 en positif :**\nVous agissez en créant, communiquant et insufflant de la joie, de l'art ou du relationnel.\n\n🙁 **Vos défauts si vous exprimez votre nombre 3 en négatif :**\nVous faites preuve d'immaturité, fuyez les responsabilités, ou vous dispersez de façon stérile.",
    4: "😊 **Vos qualités si vous utilisez votre nombre 4 en positif :**\nVous agissez par le travail, la méthode, le courage et l'organisation structurée.\n\n🙁 **Vos défauts si vous exprimez votre nombre 4 en négatif :**\nVous êtes inhibé par la peur, vous vous autolimitez ou créez des blocages rigides.",
    5: "😊 **Vos qualités si vous utilisez votre nombre 5 en positif :**\nVous agissez guidé par la nouveauté, l'audace, la curiosité et l'adaptabilité.\n\n🙁 **Vos défauts si vous exprimez votre nombre 5 en négatif :**\nVous êtes inconstant, impulsif, commencez tout sans jamais aboutir.",
    6: "😊 **Vos qualités si vous utilisez votre nombre 6 en positif :**\nVous agissez pour créer de l'harmonie, de la beauté, des améliorations et du soin.\n\n🙁 **Vos défauts si vous exprimez votre nombre 6 en négatif :**\nVous avez la colère rapide ou fuyez systématiquement face aux problèmes.",
    7: "😊 **Vos qualités si vous utilisez votre nombre 7 en positif :**\nVous agissez par l'intellect, l'analyse, l'expertise et l'originalité constructive.\n\n🙁 **Vos défauts si vous exprimez votre nombre 7 en négatif :**\nVotre sur-analyse mentale paralyse l'action, vous isolant des autres.",
    8: "😊 **Vos qualités si vous utilisez votre nombre 8 en positif :**\nVous agissez en bâtisseur puissant et structuré pour vous réaliser avec énergie.\n\n🙁 **Vos défauts si vous exprimez votre nombre 8 en négatif :**\nVous prenez une posture de victime injuste ou utilisez la violence verbale.",
    9: "😊 **Vos qualités si vous utilisez votre nombre 9 en positif :**\nVous agissez tourné vers le monde, humaniste, idéaliste et passionné.\n\n🙁 **Vos défauts si vous exprimez votre nombre 9 en négatif :**\nVous souffrez d'émotivité excessive, ou avez tendance à vous sacrifier inutilement."
}

DESC_FEUILLES = {
    1: "😊 **Vos qualités si vous utilisez votre nombre 1 en positif :**\nAutonome en amour, vous décidez pour le foyer, vous êtes le moteur constructif du couple.\n\n🙁 **Vos défauts si vous exprimez votre nombre 1 en négatif :**\nFait preuve d'égocentrisme, tyrannie domestique, ne pense qu'à ses propres plaisirs.",
    2: "😊 **Vos qualités si vous utilisez votre nombre 2 en positif :**\nPartage harmonieux, grand besoin d'union, empathie réconfortante et attentive.\n\n🙁 **Vos défauts si vous exprimez votre nombre 2 en négatif :**\nDépendance affective, effacement total de soi ou construction d'une carapace de glace.",
    3: "😊 **Vos qualités si vous utilisez votre nombre 3 en positif :**\nJoie de vivre, charme, communication fluide, séduction et humour permanent.\n\n🙁 **Vos défauts si vous exprimez votre nombre 3 en négatif :**\nSuperficialité, légèreté coupable dans l'engagement, grande immaturité.",
    4: "😊 **Vos qualités si vous utilisez votre nombre 4 en positif :**\nLoyauté indéfectible, engagement sur le long terme, apporte une sécurité absolue.\n\n🙁 **Vos défauts si vous exprimez votre nombre 4 en négatif :**\nMéfiance maladive, rigidité cassante, peur panique de l'autre ou de la trahison.",
    5: "😊 **Vos qualités si vous utilisez votre nombre 5 en positif :**\nPartenaire stimulant, adore bouger, explorer et dynamiser le couple sans cesse.\n\n🙁 **Vos défauts si vous exprimez votre nombre 5 en négatif :**\nInstabilité chronique, infidélité par ennui, comportements et réactions excessifs.",
    6: "😊 **Vos qualités si vous utilisez votre nombre 6 en positif :**\nCocon chaleureux, sens de la famille, recherche d'un amour unique, harmonieux et stable.\n\n🙁 **Vos défauts si vous exprimez votre nombre 6 en négatif :**\nExigence de perfection étouffante, jalousie, fuite lâche face aux conflits.",
    7: "😊 **Vos qualités si vous utilisez votre nombre 7 en positif :**\nPartenaire intellectuel, respect profond du jardin secret de l'autre, calme partagé.\n\n🙁 **Vos défauts si vous exprimez votre nombre 7 en négatif :**\nRepli dans sa caverne, silence radio prolongé, attitude de supériorité hautaine.",
    8: "😊 **Vos qualités si vous utilisez votre nombre 8 en positif :**\nProtecteur courageux, force de construction matérielle et psychologique pour le foyer.\n\n🙁 **Vos défauts si vous exprimez votre nombre 8 en négatif :**\nIntransigeance, rapports de force permanents, dureté verbale ou froideur.",
    9: "😊 **Vos qualités si vous utilisez votre nombre 9 en positif :**\nAmour universel, dévouement sans faille, idéalisme romantique magnifique.\n\n🙁 **Vos défauts si vous exprimez votre nombre 9 en négatif :**\nDésillusions permanentes, sentiment de s'être sacrifié pour rien, exigence d'absolu.",
    11: "😊 **Vos qualités si vous utilisez votre nombre 11 en positif :**\nAccompagnement intuitif puissant, élévation mutuelle, soutien sans faille du partenaire.\n\n🙁 **Vos défauts si vous exprimez votre nombre 11 en négatif :**\nFusion destructrice, manipulation subtile ou exigence relationnelle intenable.",
    22: "😊 **Vos qualités si vous utilisez votre nombre 22 en positif :**\nBâtisseur d'un couple extrêmement solide, visionnaire et protecteur pour son foyer.\n\n🙁 **Vos défauts si vous exprimez votre nombre 22 en négatif :**\nDureté implacable, autorité excessive ou repli dépressif profond en cas de crise."
}

DESC_FRUITS = {
    1: "😊 **Vos qualités si vous utilisez votre nombre 1 en positif :**\nPionnier, avant-gardiste, leadership reconnu, vous aimez arriver en tête.\n\n🙁 **Vos défauts si vous exprimez votre nombre 1 en négatif :**\nÉgocentré, autoritaire, vous vous enlisez par manque total d'initiative.",
    2: "😊 **Vos qualités si vous utilisez votre nombre 2 en positif :**\nSecond précieux, vous faites grandir les projects en binôme discret et collaboratif.\n\n🙁 **Vos défauts si vous exprimez votre nombre 2 en négatif :**\nDoute chronique de votre valeur, sous-estimation systématique de vos capacités.",
    3: "😊 **Vos qualités si vous utilisez votre nombre 3 en positif :**\nCréateur de liens, de concepts, d'art, vous possédez un dynamisme public exceptionnel.\n\n🙁 **Vos défauts si vous exprimez votre nombre 3 en négatif :**\nÉparpillement professionnel, manque cruel de profondeur et de sérieux dans vos tâches.",
    4: "😊 **Vos qualités si vous utilisez votre nombre 4 en positif :**\nMéthodique, rigoureux, vous posez des fondations inébranlables pour la réussite.\n\n🙁 **Vos défauts si vous exprimez votre nombre 4 en négatif :**\nCadre étriqué, maniaquerie stérile, peur paralysante du risque professionnel.",
    5: "😊 **Vos qualités si vous utilisez votre nombre 5 en positif :**\nInnovateur agile, vous adorez les grands changements, décodez de nouveaux défis.\n\n🙁 **Vos défauts si vous exprimez votre nombre 5 en négatif :**\nAttitude velléitaire, vous commencez tout sans jamais rien structurer ni terminer.",
    6: "😊 **Vos qualités si vous utilisez votre nombre 6 en positif :**\nSoignant, vous apportez des solutions harmonieuses, éthiques et concrètes.\n\n🙁 **Vos défauts si vous exprimez votre nombre 6 en négatif :**\nVous fuyez les explications nécessaires ou déclenchez d'inutiles guerres d'ego.",
    7: "😊 **Vos qualités si vous utilisez votre nombre 7 en positif :**\nExpert original, vous transmettez votre savoir, vos analyses et votre singularité.\n\n🙁 **Vos défauts si vous exprimez votre nombre 7 en négatif :**\nVous vous sentez incompris, rejeté ou vous vous isolez volontairement de votre marché.",
    8: "😊 **Vos qualités si vous utilisez votre nombre 8 en positif :**\nBâtisseur puissant, vous réussissez matériellement ou guérissez profondément les âmes.\n\n🙁 **Vos défauts si vous exprimez votre nombre 8 en négatif :**\nFrustration, sentiment d'injustice, tendance à la malhonnêteté ou au statut de victime.",
    9: """😊 **Vos qualités si vous utilisez votre nombre 9 en positif :**
Dans vos réalisations, vous êtes tourné vers le monde, au sens large.
Vous pouvez être passionné et engagé dans une cause.
Vous pouvez aussi exprimer votre ouverture et votre sensibilité en travaillant pour le service public ou une dimension collective, ou en vous tournant vers les sciences humaines et universelles.
Il est possible que vous soyez attiré par tout ce qui touche aux voyages, à la découverte de l’étrange ou de l’étranger, en travaillant à l’international.
Vous pouvez également travailler dans le domaine du luxe, du rêve, tout ce qui brille.
Enfin, par vos talents ou votre engagement, vous vous inscrivez parfois dans la vie publique.
Le fruit de valeur 9 peut favoriser la reconnaissance si :
• vous restez centré sur vos actions, votre projet, votre passion ;
• vous restez fidèle à ce que vous êtes en profondeur ;
• vous écoutez votre sensibilité, vos émotions.

🙁 **Vos défauts si vous exprimez votre nombre 9 en négatif :**
Votre côté utopiste vous fait rêver à un monde meilleur et vous rend peu réaliste.
Votre émotivité vous submerge, vous rend nerveux ou inactif, cela vous empêche d’exercer votre métier avec sérénité.
Votre besoin de reconnaissance professionnelle est tel que cela peut vous rendre agressif, voire fanatique ou dépendant.
Dans ce cas :
• Vous oubliez que la reconnaissance ou la notoriété est le résultat de vos actions. Restez concentré sur vos motivations et continuez à vous engager dans vos actions.
• Apprenez à découvrir le monde, à voyager, à agrandir vos centres d’intérêt, à vous impliquer collectivement. Le monde a besoin de votre sensibilité, de votre engagement, de votre vision.
• Osez vous tourner vers la psychologie, la philosophie, les sciences humaines, l’ésotérisme, vous avez des prédispositions pour cela.""",
    11: "😊 **Vos qualités si vous utilisez votre nombre 11 en positif :**\nSurpassement intuitif rare pour faire évoluer collectivement des structures ou personnes.\n\n🙁 **Vos défauts si vous exprimez votre nombre 11 en négatif :**\nDoutes intérieurs destructeurs, dévalorisation personnelle constante et freinante.",
    22: "😊 **Vos qualités si vous utilisez votre nombre 22 en positif :**\nVous bâtissez des réalisations majeures et colossales pour la collectivité.\n\n🙁 **Vos défauts si vous exprimez votre nombre 22 en négatif :**\nPeurs totally bloquantes, folie des grandeurs (mégalomanie) ou repli dépressif."
}

DESC_DYNAMIQUE = {
    1: "Dynamique 1 : L'atmosphère de votre vie favorise l'action, l'indépendance et le leadership.",
    2: "Dynamique 2 : L'atmosphère de votre vie favorise l'accompagnement et le binôme.",
    3: "Dynamique 3 : L'atmosphère de votre vie favorise la création et la communication.",
    4: "Dynamique 4 : L'atmosphère de votre vie favorise la construction et la méthode.",
    5: "Dynamique 5 : L'atmosphère de votre vie favorise l'innovation et l'adaptabilité.",
    6: "Dynamique 6 : L'atmosphère de votre vie favorise le soin et les responsabilités.",
    7: "Dynamique 7 : L'atmosphère de votre vie favorise la cérébralité et l'expertise.",
    8: "Dynamique 8 : L'atmosphère de votre vie favorise la réalisation et la puissance.",
    9: """**Côté international ou humain, esprit collectif**
L’ambiance qui entoure votre vie favorise un côté international ou humain, privilégiant un esprit collectif.

😊 **En positif :** globalement, l’atmosphère de votre vie favorise les voyages, votre aptitude à vous intéresser au monde, au genre humain, à œuvrer pour une cause, à effectuer des actions publiques ou pour la communauté. En fonction de ce que vous avez accompli, elle facilite la reconnaissance, voire la notoriété.

🙁 **En négatif :** cette ambiance peut entraîner un certain manque de réalisme, une forte émotivité ou nervosité. De même, elle peut engendrer un besoin de « voyager artificiellement » : alcool, drogue, etc., parfois jusqu’à en devenir dépendant.

*Exemple : Elvis Presley (Elvis Aaron Presley), né le 8/01/1935, eut une influence mondiale et considérable sur la culture musicale. Il vendit sept cent millions de disques de son vivant, et le chiffre d’un milliard est à présent évoqué, faisant de lui l’artiste solo ayant vendu le plus de disques au monde. Il donna près de mille deux cents concerts aux États-Unis. Également acteur, il fut à l’affiche de trente-trois films. Il était aussi connu pour son addiction aux médicaments.*"""
}

DESC_DEFIS = {
    "general": "Le défi met en lumière ce que vous avez à apprendre ou à dépasser pour fluidifier votre parcours. C'est un obstacle conscient ou inconscient qui, une fois traversé, devient une immense force.",
    1: """**Défi 1**
Ce défi concerne le Moi et nécessite de travailler sur votre place. En effet, vous développez trop ou pas assez d’ego.

**Analyse**
Si ce défi n’est pas relevé, comment cela se traduit-il ?
— Vous imposez vos volontés, êtes égoïste ou très autoritaire, voire tyrannique ! Vous ne pensez qu’à vos besoins immédiats sans vous soucier des dégâts collatéraux. Les autres vous indiffèrent.
**Dans ce cas :** évitez de ne penser qu’à vous et apprenez à considérer l’autre. Prenez votre place sans pour autant opprimer l’autre, en le respectant, en le considérant.

— Et/ou vous éprouvez des difficultés à aller de l’avant et à progresser, vous effectuez beaucoup d’efforts pour un résultat que vous trouvez décevant. Vous avez du mal à prendre votre place ; le dernier qui a parlé a raison. Les autres ou les faits extérieurs sont responsables de vos problèmes.
**Dans ce cas :** ne désespérez pas ; tenez compte de votre côté unique. Apprenez à décider en mettant des priorités dans l’échelle de vos besoins. Donnez-vous de petits objectifs dans un premier temps et cherchez à les tenir.
Le défi 1 est potentiellement accentué si vous n’avez pas la qualité Action (pas de lettre A, J, S).

**Que risquez-vous si vous ne faites pas d’efforts pour relever ce défi et le cultiver ?**
Vous pouvez développer une attitude excessive au point de devenir paranoïaque (méfiance envahissante des autres, car vous vous sentez menacé) ou mégalomaniaque (surestimation de vos capacités, ce qui se traduit par un désir immodéré de puissance et un amour exclusif de vous-même). Sachez qu’une fois que vous êtes dans ces comportements, il est souvent difficile d’en sortir, car le paranoïaque ou le mégalomaniaque se sert des éléments extérieurs pour alimenter son attitude.""",
    2: """**Défi 2**
Ce défi concerne « l’autre » et nécessite de travailler sur le sentiment d’abandon ou d’exclusion. Vous êtes trop ou pas assez attentif à « l’autre ».

**Analyse**
Si ce défi n’est pas relevé, comment cela se traduit-il ?
• Vous êtes complexé par rapport aux autres, indécis ou influençable. Vous avez un grand manque de confiance, êtes pétri de doutes et plein d’émotivité.
• Votre attitude de soumission face aux autres vous empêche de vous réaliser, d’agir pour vous, de penser à vous.
• Vous avez peur de l’abandon ; ce sentiment vous hante dès que vous commencez une relation.
**Dans ce cas :** apprenez à travailler en binôme pour dépasser vos doutes, à demander de l’aide à un thérapeute pour gagner en confiance. Prenez le temps de vous observer, d’apprécier vos qualités et cessez de vous dévaloriser ! La peur de l’abandon est normale pour un enfant, car il est très vulnérable. Cependant, en tant qu’adulte, ne pensez-vous pas que ces peurs n’ont plus lieu d’être ? Cherchez à vous couper de ces ressentis qui vous handicapent dans vos relations, en prenant conscience de toutes les ressources que vous avez en tant qu’adulte.

• Ou vous ne savez pas regarder correctement l’autre, vous n’êtes pas attentif à lui et ne tenez pas compte de ses besoins. Vous êtes intolérant, cassant. Quand vous êtes déçu du comportement de l’autre, vous avez tendance à être sans concession ; vous ne cherchez pas à comprendre et tirez un trait sur la relation.
• Vous vous sentez isolé et avez la sensation que les autres vous rejettent.
**Dans ce cas :** apprenez à mettre un peu de patience et de douceur dans votre façon d’agir, à accorder une seconde chance ; il y a une vraie valeur ajoutée au fait de prendre le temps de s’expliquer, à être plus tolérant. Ce n’est pas parce que certaines personnes ont été dures avec vous qu’il faut obligatoirement l’être à votre tour. En effet, dans ce cas, vous entretenez un cercle vicieux.
Le défi 2 est potentiellement accentué si vous n’avez pas la qualité Regard (pas de lettre B, K, T).

**Que risquez-vous si vous ne faites pas d’efforts pour relever ce défi et le cultiver ?**
Il est possible que vous développiez un comportement excessif, au point de finir par vous exclure des autres et de vous sentir totalement rejeté. Ou vous pourriez avoir tellement peur de vous sentir abandonné que vous préféreriez ne pas vivre de relation ou mettre un terme à une histoire d’amour afin d’éviter de vous engager et de prendre le risque de souffrir.""",
    3: """**Défi 3**
Ce défi concerne la « communication » et nécessite de travailler sur la prise de parole. Vous êtes trop ou pas assez communicant.

**Analyse**
Si ce défi n’est pas relevé, comment cela se traduit-il ?
• Votre façon de parler est abrupte, trop directe. Impulsif, vous avez à cœur de vider votre sac sans vous soucier des effets produits. De même, vos mots peuvent dépasser votre pensée, être violents. Vous pouvez aussi être superficiel et parler pour ne rien dire, ce qui cache la peur que l’on connaisse votre intimité ; assumez qui vous êtes. Et si vous ne voulez pas que l’on parle de vous, intéressez-vous à l’autre, il aura sûrement quelque chose d’intéressant à partager.
**Dans ce cas :** apprenez la mesure, mettez des formes dans vos propos. Prenez conscience que les mots mal dits produisent souvent un effet boomerang : si vous ne le faites pas pour l’autre, faites-le pour vous ! Apprenez à canaliser votre impulsivité verbale en vous forçant à l’écoute. Avant de parler ou de répondre, réfléchissez aux conséquences de vos propos. Comment prendriez-vous cela si l’on vous disait la même chose ?

• Ou d’une grande timidité surtout pendant l’enfance, vous rougissez comme une pivoine dès que l’on vous demande de vous exprimer. Vous êtes renfermé sur vous-même et le fait de prendre la parole devant les autres vous met mal à l’aise. Vous avez tendance à l’introversion.
**Dans ce cas :** exercez-vous à prendre la parole devant un public bienveillant, apprenez à dire les choses au fur et à mesure, au lieu de tout garder pour vous ; cela libère ! Sortez de la croyance que vous n’êtes pas intéressant ou que vous ne savez pas prendre la parole. Peut-être que les occasions de vous exprimer en public ont été réduites et expliquent vos peurs. Comme la marche ou l’écriture, tout s’obtient en y travaillant. Pour cela, faites du chant, du théâtre, toute activité orale.
Le défi 3 est potentiellement accentué si vous ne possédez pas la qualité Communication (pas de lettre C, L, U).

**Que risquez-vous si vous ne faites pas d’efforts pour relever ce défi et le cultiver ?**
Vous pourriez développer un comportement excessif au point de vous bloquer dans du mutisme, une grande introversion. Ou vous pourriez être catalogué grande gueule et risquer de perdre toute crédibilité et de ne plus être écouté. Dans les deux cas, ces comportements vont vous isoler.""",
    4: """**Défi 4**
Ce défi concerne « le travail, l’ordre » et nécessite de travailler sur le sentiment de culpabilité, le rapport au travail. En effet, vous travaillez trop ou pas assez ; vous êtes trop ou pas assez ordonné.

**Analyse**
Si ce défi n’est pas relevé, comment cela se traduit-il ?
• Vous travaillez tellement que vous en oubliez de vivre ! Votre besoin de perfectionnisme ou votre sens du détail tourne à l’obsession.
• Vous avez peur de manquer, de l’échec ou de la réussite.
• Vous pouvez être maniaque ; tout doit être carré et parfait, au point parfois de développer des TOC (troubles obsessionnels compulsifs).
**Dans ce cas :** apprenez à vous libérer de la peur de mal faire, organisez-vous pour établir des priorités et suivez-les, cherchez à inclure dans votre timing des récréations pour apprendre à reposer votre corps et à devenir plus efficace. Vous travaillerez mieux si vous êtes en bonne santé. Comprenez que lorsque l’on passe beaucoup de temps à vérifier, à contrôler, à rendre parfait, on finit par ne jamais aboutir et par perdre du concret dans les actions, car on se noie dans les détails. Enfin, cessez d’anticiper le résultat : les peurs viennent de ce que l’on imagine en négatif : si je fais ceci, il va m’arriver cela… En vivant l’instant présent, les peurs s’envolent.

• Ou vous avez une forte tendance à la procrastination (à remettre au lendemain) ou à l’oisiveté. Vous avez beaucoup de difficultés à travailler avec constance. Vous commencez et laissez tout en plan.
• Vous êtes désordonné et vivez dans un capharnaüm.
• Vous vous laissez aller et ne prenez pas soin de vous.
**Dans ce cas :** apprenez à vous structurer, à vous organiser ; faites une liste de vos objectifs de la journée et apprenez à la suivre, et tenez vos résolutions ; vous gagnerez en paix intérieure. Goûtez à la satisfaction de ranger au fur et à mesure : en Chine, il est coutume de dire que le désordre d’une pièce engendre de la confusion pour la personne qui l’occupe. Si vous subissez votre vie, commencez par ranger et par mettre de l’ordre dans votre habitat au lieu de chercher des méthodes compliquées pour vous en sortir.
Le défi 4 est potentiellement accentué si vous n’avez pas la qualité Travail (pas de lettre D, M, V).

**Que risquez-vous si vous ne faites pas d’efforts pour relever ce défi et le cultiver ?**
Vous pourriez développer un comportement excessif au point de ressentir un sentiment de culpabilité permanent :
• parce que vous travaillez trop ou pas assez ;
• parce que vous ne prenez pas soin de vous et ne faites rien pour changer ;
• parce que vous vous bloquez dans une attitude et ne savez pas en sortir.
Vous pourriez même vous sentir coupable de l’attitude des membres de votre entourage, de leur choix de vie, de leurs malheurs ; ou encore culpabiliser d’être heureux, etc. Chacun doit assumer ses actes, alors apprenez à être responsable, pas coupable !""",
    5: """**Défi 5**
Ce défi concerne la « liberté » et nécessite de travailler sur votre impulsivité, vos résistances. Vous avez trop ou pas assez de liberté.

**Analyse**
Si ce défi n’est pas relevé, comment cela se traduit-il ?
• Vous avez besoin d’expérimenter et de vivre à fond votre besoin de liberté, en vous mettant en danger, en prenant des risques importants.
• Vous êtes très impulsif et vous intéressez peu aux conséquences de vos actes.
• Votre besoin de tout essayer et de tout vivre peut vous faire perdre vos repères et vous entraîner dans des dépendances sans vous en rendre compte (alcool, drogue, nourriture, sexe, jeu, affectif, etc.) ou des comportements affectifs instables.
**Dans ce cas :** apprenez la modération. Ayez conscience des risques que vous prenez et soyez plus mature, moins inconséquent. Pour cela, il est nécessaire de porter un regard nouveau sur votre vie, en changeant de l’intérieur : vous avez de la valeur ! En allant dans les excès de comportement, comprenez que les gens auxquels vous tenez pourraient s’éloigner de vous à cause de votre côté ingérable. Apprenez à écouter autre chose que vos pulsions.

— Ou face à une insatisfaction affective ou professionnelle, vous résistez aux changements, préférez rester dans vos habitudes et oubliez de provoquer les ouvertures nécessaires telles que libérer la parole, changer d’attitude ou de métier, de comportement, être audacieux…
**Dans ce cas :** libérez-vous de vos chaînes mentales et de vos croyances, utilisez votre curiosité pour aborder la vie sous un nouvel angle. Regardez vos peurs en face, évaluez-les, et vous vous rendrez compte que vos risques sont finalement limités. Être en phase avec sa vraie nature apporte un vrai bénéfice qui demande un certain courage.
Le défi 5 est potentiellement accentué si vous n’avez pas la qualité Homme et Liberté (pas de lettre E, N, W).

**Que risquez-vous si vous ne faites pas d’efforts pour relever ce défi et le cultiver ?**
Vous pourriez développer un comportement excessif, au point de vous perdre dans les plaisirs immédiats qui vont vous éloigner de vous-même ; ou encore être dans l’abnégation de votre vie (renoncement partiel ou complet à vous-même et à vos intérêts personnels). Dans les deux cas, cela créera de la frustration et un sentiment d’injustice. Vous penserez être victime d’un système alors que vous serez devenu victime de vous-même.""",
    6: """**Défi 6**
Ce défi concerne la « responsabilité » et nécessite de travailler sur votre part de responsabilité. En effet, vous prenez trop ou pas assez de responsabilités.

**Analyse**
Si ce défi n’est pas relevé, comment cela se traduit-il ?
• Vous acceptez tout sans sourcillier ; vous portez votre croix et vous sentez responsable de la Terre entière ! Souvent, par souci de perfection, par sens du devoir ou besoin de tout contrôler, vous vous mettez dans des situations où les obligations professionnelles ou familiales sont trop lourdes à porter.
**Dans ce cas :** la responsabilité se partage, ne cherchez pas à tout porter. Vous allez vous épuiser ! Apprenez à déléguer, même si ce n’est pas parfait. Apprenez à connaître vos limites pour ne pas vous effondrer sous la tâche. Et surtout, expérimentez le lâcher-prise. Votre vie deviendra moins lourde !

— Ou vous n’avez jamais tort et n’êtes responsable de rien. Vous n’assumez pas vos actes et cherchez à vous dédouaner de tout.
• Vous manipulez les faits, les mots ou votre entourage pour ne pas être pris en faute.
**Dans ce cas :** assumez vos responsabilités et pour cela, n’oubliez pas qu’être responsable, c’est passer du mode enfant au mode adulte. Apprenez à reconnaître vos torts ! Vous verrez, la tension tombe immédiatement, alors que les nier met de l’huile sur le feu.
Le défi 6 est potentiellement accentué si vous n’avez pas la qualité Femme (pas de lettre F, O, X).

**Que risquez-vous si vous ne faites pas d’efforts pour relever ce défi et le cultiver ?**
Vous pourriez développer un comportement excessif au point de crouler sous les charges et de vous exténuer, et de finir par reprocher aux autres de ne pas en faire assez. Comprenez que c’est votre comportement qui a induit cela.
Ou, à force de revendiquer que vous n’êtes responsable de rien, vous pourriez ne jamais grandir mentalement, tel un enfant qui dit : « C’est pas moi, c’est lui ! » De plus, lorsque la vérité est découverte, vous risquez de passer pour quelqu’un de malhonnête et plus personne ne prendra vos dires au sérieux.""",
    7: """**Défi 7**
Ce défi concerne la « confiance en soi » et nécessite de travailler sur le sentiment d’infériorité ou de supériorité, et donc d’isolement. Vous avez trop ou pas assez confiance en vous.

**Analyse**
Si ce défi n’est pas traité, comment cela se traduit-il ?
• Vous avez une haute estime de ce que vous voulez réaliser, à tel point que parfois la peur d’être médiocre pourrait annuler vos initiatives.
• Vous avez tendance à regarder les autres de haut, en les critiquant. Vous avez une haute opinion de vous-même (orgueil) et cherchez à la cacher derrière de la fausse modestie.
**Dans ce cas :** votre sentiment de supériorité est une parade pour cacher un grand manque de confiance en vous et en les autres. Acceptez de vous ouvrir davantage et soyez plus généreux envers vous et les autres. Pour atteindre votre souhait de belles réalisations, vous devez tout d’abord travailler la confiance en vous, pour ne pas vous bloquer en cours de route. Travaillez sur vous en profondeur, pour connaître vos talents, le sens de votre vie et les doutes partiront.

— Ou vous êtes mal dans votre peau ; vous ne vous aimez pas, développez du pessimisme et de l’anxiété liés à un problème de confiance en vous. Vous vous sentez différent, incompris et seul.
**Dans ce cas :** développez votre singularité, assumez votre différence, votre originalité. Plus vous allez travailler sur vous en profondeur, plus vous prendrez conscience de vos atouts et de vos capacités, et plus vous apprendrez à vous aimer tel que vous êtes. Formez-vous, faites un bilan de compétences, regardez l’échec différemment : comme une chance de ne plus reproduire vos erreurs en tenant compte de cette expérience.
Le défi 7 est potentiellement accentué si vous n’avez pas la qualité Apprentissage et Spiritualité (pas de lettre G, P, Y).

**Que risquez-vous si vous ne faites pas d’efforts pour relever ce défi et le cultiver ?**
En raison d’un sentiment d’infériorité ou de supériorité exagéré, vous pourriez développer un comportement excessif, au point de vous retrancher dans votre monde et de finir par vous condamner à l’isolement et à la solitude. Le sentiment d’être incompris, de ne pas vivre sur la même planète que les autres peut aller même jusqu’à faire naître chez vous une certaine misanthropie (le fait de détester et de mépriser le genre humain).""",
    8: """**Défi 8**
Ce défi concerne la « réalisation » et nécessite de travailler sur le sentiment de légitimité. En effet, vous vous sentez trop ou pas assez légitime.

**Analyse**
Si ce défi n’est pas dépassé, comment cela se traduit-il ?
• Votre carrière, vos réalisations sont le centre de toutes vos attentions et discussions.
• Vous êtes obnubilé par votre ambition, votre statut social, le besoin de prendre le pouvoir ou le fait d’avoir beaucoup d’argent.
• Vous utilisez des moyens douteux pour parvenir à vos fins : mensonges, manipulations, dureté, arrivisme, malhonnêteté, violence.
**Dans ce cas :** le fait d’être focalisé sur votre carrière ou vos ambitions démontre, malgré ce que l’on pourrait penser, un déficit de légitimité. Vous cherchez à la démontrer par tous les moyens, car vous avez, inconsciemment, une faible estime de soi. Prenez votre place, exprimez votre ressenti et prenez conscience de votre valeur. Comprenez que se réaliser, c’est avec les autres et non contre les autres. De même, utiliser des moyens malhonnêtes pour assouvir vos fins est une attitude très court-termiste. Réfléchissez à votre rapport à l’argent, qui doit prendre une place juste et équilibrée dans votre vie.

• Ou vous manquez d’ambition, de capacité de réalisation ; vous n’avez pas de projet.
• Régulièrement, vous ressentez un sentiment d’injustice, de frustration au niveau personnel et/ou professionnel. Vous vous sentez victime d’une personne, d’une structure ou d’une institution.
• Vous faites des achats compulsifs, vous êtes avare ou dépensier.
**Dans ce cas :** apprenez à exprimer ce que vous souhaitez ; expliquez votre ressenti sans violence ; apprenez à vous réaliser. Les sentiments d’injustice ou de frustration proviennent d’une place que l’on n’a pas su prendre, alors prenez-la, exprimez votre légitimité en travaillant avec persévérance et surtout faites-vous respecter. Personne ne fera tout cela à votre place.
Décidez de sortir de votre attitude je-n’ai-vraiment-pas-de-chance, qui vous empêche de vous remettre en question. Si vous le souhaitez, cette attitude peut s’inverser si vous sortez de votre autocentrage et apprenez à voir le verre à moitié plein !
Votre rapport compliqué à l’argent est l’expression d’un manque de valeur : vous le jetez, car vous ne valez rien ; ou vous le gardez, car vous pensez qu’ainsi, vous valez plus.
Le défi 8 est potentiellement accentué si vous n’avez pas la qualité Réalisation (pas de lettre H, Q, Z).

**Que risquez-vous si vous ne faites pas d’efforts pour relever ce défi et le cultiver ?**
Vous pourriez adopter un comportement excessif, au point de développer le « complexe de Caliméro » (c’est trop injuste… tout le monde est contre moi…) et de vous enfermer dans ce rôle.
Ou vous pourriez vous mettre dans une situation de bourreau-victime au niveau personnel et/ou professionnel en oubliant de réagir, de demander de l’aide.
Enfin, s’il y a eu malhonnêteté, vous pourriez connaître une chute sociale et/ou financière.""",
    9: """**Défi 9 (ou 0)**
Ce défi concerne les « autres » et nécessite de travailler sur votre regard sur le monde. En effet, vous êtes trop ou pas assez dans l’émotion.

**Analyse**
Si ce défi n’est pas dépassé, comment cela se traduit-il ?
— Vous vous laissez envahir par les problèmes des autres et du monde. Vous êtes ultrasensible, affecté par le mal-être qui vous entoure, ou par l’ambiance chaotique du monde. Ce que vous ressentez de l’extérieur occupe une telle place que vous pourriez oublier de vivre pleinement votre vie, négliger votre quotidien et finir par déprimer.
**Dans ce cas :** apprenez à canaliser votre émotion en faisant du yoga, de la méditation, du sport. Passionnez-vous pour une cause, une action. Vous pourrez ainsi déplacer les vagues émotionnelles sur un projet, une idée. Comprenez que votre sensibilité doit être mise au service de l’amélioration du monde, même à toute petite échelle.

— Ou vous ne ressentez quasi rien, êtes détaché de toute émotion, les problèmes des autres glissent sur vous. Vous avez tendance à être insensible et pourriez manquer d’humanité.
**Dans ce cas :** la carapace émotionnelle que vous avez construite pour vous protéger, vous éloigne des autres. Apprenez à développer l’altruisme et la compréhension d’autrui, sans pour autant absorber toute la détresse alentour. Avoir de la compassion, ce n’est pas épouser ou prendre les problèmes de l’autre, c’est être capable de regarder la souffrance de l’autre pour l’aider à s’en sortir. Après une bonne action, vous aurez la sensation d’avoir grandi.
Le défi 9 est potentiellement accentué si vous n’avez pas la qualité Groupe (pas de lettre I, R).

**Que risquez-vous si vous ne faites pas d’efforts pour relever ce défi et le cultiver ?**
Pour éviter d’être submergé par les émotions, vous pourriez vous enfermer dans des états parallèles en recherchant du bien-être artificiel (médicaments, drogue, alcool, etc.), ou en vous créant un monde imaginaire (mythomane). Prenez conscience que ces comportements peuvent vous entraîner loin du monde réel ou développer encore plus de peur et de mal-être quand vous aurez retrouvé votre état normal.
Ou vous pourriez vous construire une muraille affective, en développant des phobies vis-à-vis des tiers : agoraphobe (peur de la foule) ou raciste (peur de l’étranger)."""
}
DESC_DEFIS[0] = DESC_DEFIS[9]

DESC_MEMOIRES = {
    13: "⚠️ **MÉMOIRE FAMILIALE 13 (Constriction/Blocage)** : Oscille entre travail acharné et blocage par la peur.",
    14: "⚠️ **MÉMOIRE FAMILIALE 14 (Liberté/Instabilité)** : Héritage lié aux excès ou contraintes. Risque d'impulsivité ou dépendances.",
    16: "⚠️ **MÉMOIRE FAMILIALE 16 (Affect/Isolement)** : Schémas relationnels complexes. Entraîne un besoin d'isolement et un orgueil bouclier.",
    19: "⚠️ **MÉMOIRE FAMILIALE 19 (Ego/Action)** : Sentiment d'être 'seul contre tous'. Provoque de l'orgueil et d'intenses rapports de force."
}

DESC_ANNEE_PERSO = {
    1: "Année 1 : Nouveau départ, initiatives, action et lancement de cycle.",
    2: "Année 2 : Patience, diplomatie, association, couple et écoute.",
    3: "Année 3 : Communication, créativité, relationnel et vie sociale.",
    4: "Année 4 : Travail rigoureux, organisation, construction et structure.",
    5: "Année 5 : Changement, liberté, mouvement et remise en question.",
    6: "Année 6 : Foyer, amour, responsabilités familiales et harmonie.",
    7: "Année 7 : Introspection, calme, spiritualité et bilan intellectuel.",
    8: "Année 8 : Puissance matérielle, récolte financière, karma et justice.",
    9: "Année 9 : Clôture de cycle, grand nettoyage, bilans et lâcher-prise."
}

# ==========================================
# 2. LOGIQUE MATHÉMATIQUE ET OUTILS
# ==========================================

def enlever_accents(texte):
    texte_normalise = unicodedata.normalize('NFKD', texte)
    return "".join([c for c in texte_normalise if not unicodedata.combining(c)]).upper()

def traquer_memoire(valeur, liste_fortes, liste_faibles, origine, est_fort):
    if valeur in (13, 14, 16, 19):
        info = {"valeur": valeur, "origine": origine}
        if est_fort: liste_fortes.append(info)
        else: liste_faibles.append(info)

def reduire_et_traquer(nombre, liste_fortes, liste_faibles, origine, est_fort, inclure_maitres=True):
    traquer_memoire(nombre, liste_fortes, liste_faibles, origine, est_fort)
    temp = nombre
    while temp > 9:
        if inclure_maitres and temp in (11, 22, 33):
            break
        temp = sum(int(chiffre) for chiffre in str(temp))
        traquer_memoire(temp, liste_fortes, liste_faibles, origine, est_fort)
    return temp

def somme_lettres(texte, filtre=None):
    texte = enlever_accents(texte)
    total = 0
    for char in texte:
        if 'A' <= char <= 'Z':
            if filtre is None or char in filtre:
                total += (ord(char) - ord('A')) % 9 + 1
    return total

def analyser_identite(prenoms, nom, fortes, faibles):
    mots = (prenoms + " " + nom).split()
    tot_g = tot_v = tot_c = tot_b = 0
    voyelles = ['A', 'E', 'I', 'O', 'U', 'Y']
    
    for mot in mots:
        txt = enlever_accents(mot)
        tot_b += txt.count('A') + txt.count('J') + txt.count('S')
        
        s_m = somme_lettres(mot)
        s_v = somme_lettres(mot, filtre=voyelles)
        s_c = somme_lettres(mot, filtre=[chr(i) for i in range(ord('A'), ord('Z')+1) if chr(i) not in voyelles])
        
        reduire_et_traquer(s_m, fortes, faibles, f"Mot '{mot}'", False)
        reduire_et_traquer(s_v, fortes, faibles, f"Voyelles de '{mot}'", False)
        reduire_et_traquer(s_c, fortes, faibles, f"Consonnes de '{mot}'", False)
        
        tot_g += s_m
        tot_v += s_v
        tot_c += s_c
        
    r2 = reduire_et_traquer(tot_g, fortes, faibles, "Racine 2 (Nom complet)", True)
    feu = reduire_et_traquer(tot_v, fortes, faibles, "Feuilles (Voyelles)", True, inclure_maitres=True)
    fru = reduire_et_traquer(tot_c, fortes, faibles, "Fruits (Consonnes)", True, inclure_maitres=True)
    bra = reduire_et_traquer(tot_b, fortes, faibles, "Branches (Lettres A,J,S)", True, inclure_maitres=False)
    
    return r2, feu, fru, bra

def analyser_date(jour, mois, annee, fortes, faibles):
    j, m, a = int(jour), int(mois), int(annee)
    
    reduire_et_traquer(j, fortes, faibles, "Jour de naissance", True, inclure_maitres=True)
    reduire_et_traquer(m, fortes, faibles, "Mois de naissance", False, inclure_maitres=True)
    reduire_et_traquer(sum(int(c) for c in str(a)), fortes, faibles, "Année de naissance", False, inclure_maitres=True)
    
    eco = reduire_et_traquer(j, fortes, faibles, "Écorce (Jour)", True, inclure_maitres=True)
    tr = reduire_et_traquer(j + m, fortes, faibles, "Tronc (Jour + Mois)", True)
    
    date_chiffres = sum(int(c) for c in f"{jour}{mois}{annee}" if c.isdigit())
    r1 = reduire_et_traquer(date_chiffres, fortes, faibles, "Racine 1 (Date complète)", True)
    
    return r1, tr, eco

def calculer_defi(jour, mois, annee):
    j_red = sum(int(c) for c in str(jour))
    while j_red > 9: j_red = sum(int(c) for c in str(j_red))
    m_red = sum(int(c) for c in str(mois))
    while m_red > 9: m_red = sum(int(c) for c in str(m_red))
    defi = abs(j_red - m_red)
    return defi, j_red, m_red

def calculer_annee_personnelle(tronc, annee_cible):
    somme = tronc + sum(int(c) for c in str(annee_cible))
    while somme > 9:
         somme = sum(int(c) for c in str(somme))
    return somme

def fusionner_memoires(liste):
    groupes = {}
    for m in liste:
        val = m["valeur"]
        if val not in groupes: groupes[val] = set()
        groupes[val].add(m["origine"])
    return groupes

# ==========================================
# 3. INTERFACE WEB STREAMLIT
# ==========================================

st.set_page_config(page_title="Numérologie - Arbre de Vie", layout="centered")

st.title("🌳 Votre Arbre de Vie Numérologique")
st.write("Méthode intégrale basée sur l'ouvrage de Lydie Castells et Didier Durandy.")

with st.form("formulaire_numerologie"):
    prenoms = st.text_input("Tous vos prénoms (séparés par un espace)", value="Stéphane Robert François")
    nom = st.text_input("Votre NOM de naissance", value="Boukobza")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        jour = st.text_input("Jour de naissance (ex: 23)", value="23")
    with col2:
        mois = st.text_input("Mois (ex: 03)", value="03")
    with col3:
        annee = st.text_input("Année (ex: 1981)", value="1981")
        
    submit_button = st.form_submit_button("Générer mon arbre")

if submit_button and prenoms and nom and jour and mois and annee:
    
    mem_fortes_brutes = []
    mem_faibles_brutes = []
    
    r1, tr, eco = analyser_date(jour, mois, annee, mem_fortes_brutes, mem_faibles_brutes)
    r2, feu, fru, bra = analyser_identite(prenoms, nom, mem_fortes_brutes, mem_faibles_brutes)
    
    r1_s = sum(int(c) for c in str(r1)) if r1 > 9 else r1
    r2_s = sum(int(c) for c in str(r2)) if r2 > 9 else r2
    tr_s = sum(int(c) for c in str(tr)) if tr > 9 else tr
    traquer_memoire(r1_s + r2_s + tr_s, mem_fortes_brutes, mem_faibles_brutes, "Calcul intermédiaire Dynamique de vie", True)
    
    dyn = reduire_et_traquer(r1 + r2 + tr, mem_fortes_brutes, mem_faibles_brutes, "Dynamique de vie", True)
    defi, j_r, m_r = calculer_defi(jour, mois, annee)
    
    annee_en_cours = datetime.date.today().year
    annee_personnelle = calculer_annee_personnelle(tr, annee_en_cours)

    fortes = fusionner_memoires(mem_fortes_brutes)
    faibles = fusionner_memoires(mem_faibles_brutes)
    for val in list(fortes.keys()):
        if val in faibles:
            fortes[val].update(faibles[val])
            del faibles[val]

    # --- GÉNÉRATION DE L'IMAGE ---
    img_trouvee = False
    for img_name in ["image_b81b3e.jpg", "image_c641ff.png", "image_c6a3f9.png", "image_c7943a.jpg", "image_c79e5f.jpg", "arbre_vierge.png", "arbre_vierge.jpg", "arbre.png"]:
        if os.path.exists(img_name):
            img_originale = Image.open(img_name).convert("RGBA")
            img = Image.new("RGB", img_originale.size, (255, 255, 255))
            img.paste(img_originale, (0, 0), img_originale)
            W, H = img.size
            img_trouvee = True
            break
            
    if img_trouvee:
        draw = ImageDraw.Draw(img)
        try: 
            font_large = ImageFont.truetype("arial.ttf", 65)
            font_small = ImageFont.truetype("arial.ttf", 45)
        except OSError: 
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        positions = {
            "R1": (W * 0.41, H * 0.89, formater_cle(r1)),
            "R2": (W * 0.59, H * 0.89, formater_cle(r2)),
            "TR": (W * 0.50, H * 0.77, formater_cle(tr)),
            "EC": (W * 0.50, H * 0.60, formater_cle(eco)),
            "BR": (W * 0.32, H * 0.41, formater_cle(bra)),
            "FE": (W * 0.68, H * 0.41, formater_cle(feu)),
            "FR": (W * 0.50, H * 0.24, formater_cle(fru))
        }

        for k, (x_c, y_c, txt) in positions.items():
            current_font = font_small if len(txt) > 2 else font_large
            bbox = draw.textbbox((0, 0), txt, font=current_font)
            draw.text((x_c - (bbox[2]-bbox[0])/2, y_c - (bbox[3]-bbox[1])/2), txt, fill="black", font=current_font)
        
        st.success(f"Calculs terminés pour {prenoms.split()[0].capitalize()} !")
        st.image(img, caption="Votre Arbre de Vie", use_container_width=True)
    else:
        st.warning("Image de l'arbre absente. Arbre géométrique de secours généré.")
        img = Image.new("RGB", (800, 1000), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.polygon([(400, 500), (200, 950), (600, 950)], fill="#1a1c4b")
        
        try: 
            font_large_secours = ImageFont.truetype("arial.ttf", 50)
            font_small_secours = ImageFont.truetype("arial.ttf", 35)
        except OSError: 
            font_large_secours = ImageFont.load_default()
            font_small_secours = ImageFont.load_default()
            
        pos = [(328, 890, r1), (472, 890, r2), (400, 770, tr), (400, 600, eco), (256, 410, bra), (544, 410, feu), (400, 240, fru)]
        for x, y, val in pos:
            txt_val = formater_cle(val)
            draw.ellipse([(x-50, y-50), (x+50, y+50)], fill="#FFC000")
            current_font_secours = font_small_secours if len(txt_val) > 2 else font_large_secours
            bbox = draw.textbbox((0,0), txt_val, font=current_font_secours)
            draw.text((x - (bbox[2]-bbox[0])/2, y - (bbox[3]-bbox[1])/2), txt_val, fill="black", font=current_font_secours)
        st.image(img, use_container_width=True)

    # --- AFFICHAGE TEXTUEL INTEGRAL ---
    st.header("📖 Interprétation Complète du Profil")
    
    st.subheader("⛓️ Mémoires Familiales (Blocages inconscients)")
    if len(fortes) == 0 and len(faibles) == 0:
        st.success("✅ Aucun blocage familial n'a été détecté.")
    else:
        if len(fortes) > 0:
            st.markdown("### 🔴 MÉMOIRES FORTES (Impact direct sur vos piliers)")
            for val, origines in sorted(fortes.items()):
                st.error(f"**{DESC_MEMOIRES[val]}**\n\n*📌 Provenance :* " + ", ".join(origines))
                
        if len(faibles) > 0:
            st.markdown("### 🟠 Mémoires Faibles (Présentes en filigrane dans vos calculs)")
            for val, origines in sorted(faibles.items()):
                st.warning(f"**{DESC_MEMOIRES[val]}**\n\n*📌 Provenance :* " + ", ".join(origines))

    st.markdown("---")
    
    st.subheader("🔺 Le Triangle Fondamental (Vos besoins essentiels)")
    r1_key = formater_cle(r1) if r1 in (11, 22, 33) else r1
    r2_key = formater_cle(r2) if r2 in (11, 22, 33) else r2
    tr_key = formater_cle(tr) if tr in (11, 22, 33) else tr
    dyn_key = formater_cle(dyn) if dyn in (11, 22, 33) else dyn
    eco_key = int(jour) if int(jour) <= 9 else reduire_et_traquer(int(jour), [], [], "", False, False)
    
    st.info(f"**1re Racine (Date de naissance) : {r1_key}**\n\n{DESC_RACINES.get(r1, DESC_RACINES.get(r1_s, ''))}")
    st.info(f"**2de Racine (Identité complète) : {r2_key}**\n\n{DESC_RACINES.get(r2, DESC_RACINES.get(r2_s, ''))}")
    st.info(f"**Tronc (Objectif de vie) : {tr_key}**\n\n{DESC_TRONC.get(tr, DESC_TRONC.get(tr_s, ''))}")
    
    st.markdown("---")
    
    st.subheader("🌿 La Sève (Orientation générale)")
    st.info(f"**Dynamique de vie : {dyn_key}**\n\n{DESC_DYNAMIQUE.get(dyn, DESC_DYNAMIQUE.get(sum(int(c) for c in str(dyn)), ''))}")

    st.markdown("---")
    
    st.subheader("🍃 Les 4 Clés du comportement")
    
    eco_val_red = sum(int(c) for c in str(eco)) if eco > 9 else eco
    ecorce_final_texte = f"{DESC_ECORCE_COMMUNE.get(eco_val_red, DESC_ECORCE_COMMUNE.get(eco, ''))}\n\n{DESC_ECORCE_SPECIFIQUE.get(int(jour), '')}"
    st.success(f"**Écorce (Image renvoyée) : {formater_cle(eco)}**\n\n{ecorce_final_texte}")
    
    st.success(f"**Branches (Façon d'agir) : {formater_cle(bra)}**\n\n{DESC_BRANCHES.get(bra, '')}")
    st.success(f"**Feuilles (Besoins affectifs) : {formater_cle(feu)}**\n\n{DESC_FEUILLES.get(feu, DESC_FEUILLES.get(sum(int(c) for c in str(feu)), ''))}")
    st.success(f"**Fruits (Besoins de réalisation) : {formater_cle(fru)}**\n\n{DESC_FRUITS.get(fru, DESC_FRUITS.get(sum(int(c) for c in str(fru)), ''))}")

    st.markdown("---")
    
    st.subheader("⚡ Vos Défis de Naissance")
    st.warning(f"**Défi principal identifié : {defi}**\n\n{DESC_DEFIS['general']}\n\n{DESC_DEFIS.get(defi, '')}")

    st.markdown("---")

    st.subheader(f"⏳ Temporalité pour l'année {annee_en_cours}")
    st.warning(f"**Vous êtes en Année Personnelle {annee_personnelle}.**\n\n{DESC_ANNEE_PERSO.get(annee_personnelle, '')}")
