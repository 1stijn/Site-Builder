import os
import re
import datetime
from collections import defaultdict
from colorama import init, Fore, Style

init()

TEMPLATES = {
    'jewelry.html': 'templates/jewelry.html',
    'home.html': 'templates/home.html',
    'base.html': 'templates/base.html',
    'sports.html': 'templates/sports.html',
    'pet.html': 'templates/pet.html',
    'books.html': 'templates/books.html',
    'electronics.html': 'templates/electronics.html',
    'toys.html': 'templates/toys.html',
    'clothing.html': 'templates/clothing.html',
    'food.html': 'templates/food.html',
    'outdoor.html': 'templates/outdoor.html',
    'health.html': 'templates/health.html',
    'beauty.html': 'templates/beauty.html',
    'automotive.html': 'templates/automotive.html',
    'music.html': 'templates/music.html'
}

KEYWORDS = {
    'jewerly.html': [
        'jewelry', 'jewels', 'gemstones', 'rings', 'necklaces', 'bracelets', 'earrings', 'jewelry trends', 'fine jewelry', 'luxury jewelry',
        'fashion jewelry', 'custom jewelry', 'vintage jewelry', 'designer jewelry', 'jewelry care', 'jewelry repair', 'jewelry cleaning', 'jewelry gifts', 'jewelry collections',
        'gemstones types', 'precious stones', 'semi-precious stones', 'birthstones', 'jewelry making', 'jewelry design', 'jewelry trends 2024', 'unique jewelry', 'handmade jewelry', 'jewelry brands',
        'jewelry stores', 'jewelry sales', 'jewelry auctions', 'jewelry market', 'jewelry styles', 'jewelry fashion', 'jewelry accessories', 'jewelry and watches', 'jewelry craftsmanship', 'fine gems',
        'jewelry for weddings', 'engagement rings', 'wedding bands', 'jewelry care tips', 'jewelry shopping', 'custom designs', 'jewelry for special occasions', 'jewelry inspirations', 'designer collections',
        'jewelry trends for men', 'jewelry trends for women', 'vintage jewelry trends', 'luxury jewelry trends', 'fashion jewelry trends', 'trendy jewelry', 'jewelry reviews', 'jewelry maintenance tips', 'high-end jewelry',
        'eco-friendly jewelry', 'sustainable jewelry', 'ethical jewelry', 'jewelry for gifting', 'celebrity jewelry', 'jewelry personalization', 'jewelry trends 2024', 'jewelry for all occasions', 'exclusive jewelry'
    ],
    'home.html': [
        'home', 'interior design', 'home decor', 'furniture', 'home improvement', 'home renovation', 'home accessories', 'home furnishings', 'home style', 'decorating tips',
        'home trends', 'living room ideas', 'bedroom decor', 'kitchen design', 'bathroom decor', 'home organization', 'storage solutions', 'home automation', 'smart home', 'home security',
        'home maintenance', 'home repair', 'DIY home projects', 'home cleaning', 'home comfort', 'home energy efficiency', 'home landscaping', 'home exterior', 'home aesthetics', 'home color schemes',
        'home lighting', 'home textiles', 'home furniture', 'home appliances', 'home gadgets', 'home design trends', 'home renovations 2024', 'home upgrades', 'home style ideas', 'home accents',
        'home design inspiration', 'home decor reviews', 'home organization tips', 'modern home design', 'classic home decor', 'luxury home decor', 'home improvement tips', 'home decorating ideas', 'eco-friendly home',
        'sustainable home design', 'home fashion', 'smart home gadgets', 'home technology', 'home comfort solutions', 'home trends 2024', 'home transformation', 'home design and decor', 'home design guides',
        'home accessories reviews', 'home design blogs', 'home renovation tips', 'home inspiration', 'home design trends', 'home updates', 'home design ideas', 'home decor shopping', 'home design and style'
    ],
    'base.html': [
        'website design', 'web development', 'web templates', 'HTML', 'CSS', 'JavaScript', 'website layout', 'responsive design', 'web standards', 'website structure',
        'web design trends', 'website themes', 'UI design', 'UX design', 'website functionality', 'web design elements', 'website customization', 'web design best practices', 'website frameworks', 'web design tools',
        'website navigation', 'website content', 'website accessibility', 'website performance', 'website optimization', 'web design tips', 'website maintenance', 'website redesign', 'website usability', 
        'web development frameworks', 'website coding', 'website aesthetics', 'website branding', 'web design inspiration', 'website features', 'website design guidelines', 'website usability tips', 'web design trends 2024',
        'website templates', 'HTML templates', 'CSS frameworks', 'JavaScript libraries', 'web design techniques', 'website project planning', 'web design and development', 'website design process', 'website functionality tips', 'website layout tips',
        'website design principles', 'web design for beginners', 'advanced web design', 'website design resources', 'website design ideas', 'web development best practices', 'website layout options', 'website design challenges', 'web design innovations', 'website development tools'
    ],
    'sports.html': [
        'sports', 'athletics', 'fitness', 'sports news', 'sports events', 'sports teams', 'sports gear', 'sports equipment', 'sports training', 'sports workouts',
        'sports performance', 'sports nutrition', 'sports health', 'sports injuries', 'sports recovery', 'sports coaching', 'sports competitions', 'sports leagues', 'sports schedules', 'sports scores',
        'sports results', 'sports highlights', 'sports coverage', 'sports commentary', 'sports analysis', 'sports rankings', 'sports statistics', 'sports updates', 'sports and fitness', 'sports motivation',
        'sports training programs', 'sports drills', 'sports tips', 'sports techniques', 'sports strategies', 'sports reviews', 'sports guides', 'sports and wellness', 'sports events 2024', 'sports news updates',
        'sports gear reviews', 'sports equipment tips', 'sports training tips', 'sports nutrition advice', 'sports health tips', 'sports injury prevention', 'sports recovery strategies', 'sports coaching techniques', 'sports leagues 2024', 'sports competitions updates',
        'sports event highlights', 'sports performance tips', 'sports injury recovery', 'sports and nutrition', 'sports and exercise', 'sports and lifestyle', 'sports workout plans', 'sports performance analysis', 'sports coaching tips', 'sports and health trends',
        'sports and technology', 'sports gadgets', 'sports gear trends', 'sports training tools', 'sports injuries management', 'sports and fitness innovations', 'sports recovery products', 'sports performance reviews', 'sports news and updates', 'sports gear recommendations'
    ],
    'pet.html': [
        'pets', 'animals', 'pet care', 'pet health', 'pet grooming', 'pet training', 'pet products', 'pet nutrition', 'pet behavior', 'pet safety',
        'pet supplies', 'pet accessories', 'pet adoption', 'pet breeds', 'pet vaccines', 'pet treatments', 'pet diseases', 'pet wellness', 'pet exercise', 'pet toys',
        'pet housing', 'pet training tips', 'pet behavior issues', 'pet travel', 'pet sitting', 'pet boarding', 'pet insurance', 'pet rescue', 'pet shelters', 'pet health tips',
        'pet food', 'pet feeding', 'pet diet', 'pet wellness checks', 'pet medical care', 'pet first aid', 'pet emergencies', 'pet care products', 'pet grooming tips', 'pet training techniques',
        'pet care services', 'pet adoption tips', 'pet care advice', 'pet training classes', 'pet behavior solutions', 'pet safety guidelines', 'pet care reviews', 'pet care essentials', 'pet care products reviews', 'pet nutrition advice',
        'pet health products', 'pet wellness programs', 'pet health news', 'pet care tips 2024', 'pet grooming services', 'pet training resources', 'pet behavior training', 'pet care recommendations', 'pet health solutions', 'pet adoption resources',
        'pet medical services', 'pet behavior management', 'pet travel tips', 'pet care for different pets', 'pet care for puppies', 'pet care for kittens', 'pet wellness tips', 'pet care and training', 'pet care and health', 'pet care innovations'
    ],
    'books.html': [
        'books', 'reading', 'literature', 'book reviews', 'book recommendations', 'book genres', 'book clubs', 'book sales', 'book collections', 'book events',
        'book publishing', 'book marketing', 'book trends', 'book news', 'book authors', 'book summaries', 'book discussions', 'book adaptations', 'book awards', 'book giveaways',
        'book series', 'book recommendations 2024', 'book lists', 'book reviews by genre', 'book reviews by author', 'book ratings', 'book criticism', 'book analysis', 'book recommendations by age group', 'book reading guides',
        'book genres 2024', 'book recommendations for kids', 'book recommendations for adults', 'book discussion guides', 'book reading tips', 'book-related news', 'book festivals', 'book launches', 'book industry news', 'book-related blogs',
        'book recommendations for different moods', 'book reading challenges', 'book club ideas', 'book recommendations for special occasions', 'book recommendations for different interests', 'book review blogs', 'book recommendations by popularity', 'book summaries by genre', 'book reviews by age group', 'book recommendations for gifts',
        'book store recommendations', 'book shopping tips', 'book collecting tips', 'book conservation', 'book recommendations for vacations', 'book discussion questions', 'book trends by year', 'book and film adaptations', 'book author interviews', 'book industry trends'
    ],
    'electronics.html': [
        'electronics', 'gadgets', 'tech', 'devices', 'electronics reviews', 'electronic products', 'electronics trends', 'technology news', 'tech reviews', 'electronics accessories',
        'electronics brands', 'smart devices', 'wearable technology', 'tech innovations', 'consumer electronics', 'electronics shopping', 'electronics updates', 'electronic components', 'electronics and gadgets', 'electronics for home',
        'electronics for office', 'electronics for entertainment', 'electronics for gaming', 'electronics for fitness', 'electronics buying guides', 'electronics tips', 'electronics troubleshooting', 'electronics repair', 'electronics maintenance',
        'latest electronics', 'electronics deals', 'tech gadgets', 'electronics recommendations', 'electronics and technology', 'electronics for personal use', 'electronics for business', 'tech reviews 2024', 'electronics news updates', 'electronics innovations',
        'electronics industry news', 'electronics market trends', 'electronics product launches', 'electronics and lifestyle', 'tech gadgets reviews', 'electronics for different needs', 'tech product comparisons', 'electronics and home automation', 'electronics buying tips', 'electronics maintenance tips',
        'electronics troubleshooting guides', 'tech gadget trends', 'latest electronics trends', 'electronics for professionals', 'electronics and home entertainment', 'tech product reviews', 'electronics market insights', 'electronics shopping tips', 'electronics recommendations for 2024', 'electronics and user experience',
        'electronics and health', 'tech innovations 2024', 'electronics product guides', 'tech gadget shopping', 'electronics reviews by type', 'electronics for travel', 'electronics product updates', 'latest tech gadgets', 'electronics and technology trends', 'electronics product recommendations'
    ],
    'toys.html': [
        'toys', 'children toys', 'educational toys', 'toys reviews', 'toy trends', 'toy safety', 'toy brands', 'toy categories', 'toy ideas', 'toy shopping',
        'toy collections', 'toys for toddlers', 'toys for kids', 'toys for different ages', 'toy development', 'toy innovation', 'toy recommendations', 'toy accessories', 'toys and learning', 'toys and games',
        'best toys 2024', 'toys and creativity', 'toys for special needs', 'interactive toys', 'toys for babies', 'toys for girls', 'toys for boys', 'toy reviews by type', 'toys for outdoor play',
        'toys for indoor play', 'educational games', 'toys and education', 'toys for sensory play', 'toys and development', 'toys and imagination', 'toys for toddlers', 'toy collections by age', 'toy trends and predictions', 'toy and game reviews',
        'best educational toys', 'toys for cognitive development', 'toys and motor skills', 'toy recommendations for birthdays', 'toy trends for 2024', 'interactive learning toys', 'toys and social skills', 'toy safety guidelines', 'best toys for different seasons', 'toy reviews and ratings',
        'latest toy trends', 'toy shopping tips', 'toy maintenance', 'educational toy brands', 'toys for summer fun', 'toys for winter play', 'toys for holiday gifts', 'interactive toys for kids', 'toys and family fun', 'toy buying guides'
    ],
    'clothing.html': [
        'clothing', 'fashion', 'apparel', 'clothing trends', 'clothing styles', 'clothing brands', 'clothing care', 'fashion tips', 'clothing collections', 'clothing shopping',
        'clothing reviews', 'clothing for men', 'clothing for women', 'clothing for kids', 'clothing accessories', 'clothing trends 2024', 'fashion news', 'fashion collections', 'fashion shows', 'fashion events',
        'clothing for different seasons', 'clothing for different occasions', 'clothing fit', 'fashion advice', 'fashion tips 2024', 'fashion trends', 'clothing styles for men', 'clothing styles for women', 'clothing fit and sizing',
        'fashion guides', 'fashion and comfort', 'clothing care tips', 'clothing shopping tips', 'fashion and lifestyle', 'clothing for special events', 'clothing for everyday wear', 'fashion accessories', 'clothing design', 'clothing brands reviews',
        'clothing trends and styles', 'fashion looks', 'fashion essentials', 'clothing collections by season', 'fashion shopping guides', 'fashion and trends 2024', 'clothing and personal style', 'fashion trends for different age groups', 'clothing care and maintenance', 'fashion for different body types',
        'clothing recommendations', 'clothing style guides', 'fashion and function', 'fashion updates', 'clothing trends by season', 'fashion items reviews', 'clothing for different climates', 'fashion and culture', 'clothing for formal events', 'fashion innovations'
    ],
    'food.html': [
        'food', 'recipes', 'cooking', 'food reviews', 'food trends', 'food news', 'healthy recipes', 'food preparation', 'food and nutrition', 'food blogs',
        'food and diet', 'food for different diets', 'food tips', 'food and wellness', 'food and lifestyle', 'cooking tips', 'recipe ideas', 'food ingredients', 'food and health', 'food safety',
        'food trends 2024', 'food for special diets', 'food for fitness', 'food and culture', 'recipe reviews', 'food and cooking techniques', 'food for weight loss', 'food recommendations', 'food and flavors',
        'healthy eating tips', 'cooking tips and techniques', 'recipe ideas for different occasions', 'food and drink pairings', 'cooking and baking', 'food preparation tips', 'food for different cuisines', 'food news updates', 'food and nutrition advice', 'food for different meals',
        'recipe guides', 'food for special needs', 'food and wellness trends', 'food lifestyle', 'food and health trends', 'recipe blogs', 'food industry news', 'cooking and recipe books', 'food trends by year', 'food and sustainability',
        'recipe recommendations', 'healthy cooking tips', 'food for specific diets', 'food preparation guides', 'food and taste', 'food and technology', 'recipe tips', 'food safety tips', 'food and nutrition guides', 'food and culture trends',
        'food and flavor innovations', 'food trends and predictions', 'cooking and health', 'food recommendations for special occasions', 'food and dietary needs', 'recipe ideas for different diets', 'food industry trends', 'food for holidays', 'food and beverage pairings', 'healthy eating guides'
    ],
    'outdoor.html': [
        'outdoor', 'outdoor activities', 'outdoor gear', 'outdoor adventures', 'outdoor sports', 'camping', 'hiking', 'outdoor equipment', 'outdoor gear reviews', 'outdoor safety',
        'outdoor recreation', 'outdoor fitness', 'outdoor activities for kids', 'outdoor events', 'outdoor hobbies', 'outdoor travel', 'outdoor essentials', 'outdoor planning', 'outdoor clothing', 'outdoor gear tips',
        'camping gear', 'hiking equipment', 'outdoor safety tips', 'outdoor adventure ideas', 'outdoor sports tips', 'outdoor fitness routines', 'outdoor equipment reviews', 'outdoor adventures 2024', 'outdoor gear shopping', 'outdoor recreation ideas',
        'camping and hiking tips', 'outdoor gear for different seasons', 'outdoor fitness tips', 'outdoor travel guides', 'outdoor adventure planning', 'outdoor activities reviews', 'outdoor sports events', 'outdoor gear recommendations', 'camping essentials', 'hiking safety tips',
        'outdoor activities for families', 'outdoor gear for beginners', 'outdoor adventure gear', 'camping and hiking gear', 'outdoor fitness challenges', 'outdoor sports reviews', 'outdoor activities trends', 'outdoor gear for different climates', 'outdoor event planning', 'outdoor recreation news',
        'outdoor adventure tips', 'outdoor gear maintenance', 'outdoor fitness programs', 'camping and outdoor cooking', 'outdoor travel tips', 'outdoor equipment maintenance', 'outdoor gear innovations', 'outdoor activities for different skill levels', 'outdoor adventure planning tips', 'outdoor gear and accessories'
    ],
    'health.html': [
        'health', 'wellness', 'fitness', 'medical treatments', 'health insurance', 'health and nutrition', 'wellness tips', 'disease prevention', 'health screenings', 'mental well-being',
        'physical fitness', 'health assessments', 'health research', 'health guides', 'health awareness', 'fitness tips', 'wellness guides', 'health and nutrition guides', 'fitness and exercise tips', 'health advice articles',
        'health resources for families', 'personal health care', 'public health', 'health services reviews', 'wellness activities', 'health management', 'fitness routines for beginners', 'holistic health', 'health challenges',
        'healthy living tips', 'wellness checkups', 'disease management', 'fitness and wellness news', 'preventive health care', 'health and wellness programs', 'health care providers', 'health monitoring', 'wellness resources',
        'fitness plans', 'health education', 'health solutions', 'mental health care', 'physical health tips', 'health and fitness trends', 'healthcare innovations', 'health lifestyle changes', 'health news', 'wellness innovations',
        'fitness routines', 'healthcare tips', 'wellness trends', 'health care solutions', 'fitness advice', 'health management tips', 'disease prevention tips', 'health and fitness programs', 'mental health resources', 'wellness strategies',
        'fitness solutions', 'health and lifestyle changes', 'wellness plans', 'health news updates', 'health and wellness innovations', 'fitness trends 2024', 'health management solutions', 'health care trends', 'wellness tips and guides', 'fitness and wellness advice'
    ],
    'beauty.html': [
        'beauty', 'skincare', 'makeup', 'beauty products', 'beauty tips', 'cosmetics', 'beauty routines', 'beauty trends', 'beauty advice', 'beauty brands',
        'skincare routines', 'makeup tutorials', 'beauty treatments', 'hair care', 'beauty care', 'beauty tips 2024', 'beauty hacks', 'beauty products reviews', 'cosmetic trends', 'beauty and wellness',
        'skincare products', 'makeup products', 'hair styling tips', 'beauty and personal care', 'beauty regimens', 'beauty for different skin types', 'beauty tips for different ages', 'beauty innovations', 'beauty routines for different occasions', 'beauty and fashion',
        'cosmetic reviews', 'beauty and skincare trends', 'makeup for different skin types', 'beauty product recommendations', 'hair care tips', 'beauty treatments and procedures', 'beauty and health', 'skincare tips', 'makeup tips', 'beauty care routines',
        'beauty tips for men', 'beauty tips for women', 'beauty product reviews 2024', 'skincare routines for different skin types', 'makeup tutorials and tips', 'beauty product recommendations 2024', 'hair care trends', 'beauty and personal grooming', 'cosmetic product reviews', 'beauty trends and innovations',
        'beauty and lifestyle', 'skincare and makeup routines', 'beauty and wellness tips', 'hair care products reviews', 'beauty trends and tips', 'cosmetic trends 2024', 'beauty care recommendations', 'makeup for different occasions', 'skincare tips and tricks', 'beauty advice and reviews'
    ],
    'automotive.html': [
        'automotive', 'cars', 'vehicles', 'car reviews', 'auto industry', 'car maintenance', 'car repair', 'automobile trends', 'car accessories', 'car buying tips',
        'auto parts', 'car care', 'car safety', 'car insurance', 'car technology', 'car performance', 'car brands', 'auto reviews', 'car ratings', 'auto trends',
        'automotive news', 'car maintenance tips', 'car repair guides', 'car care advice', 'automobile reviews', 'auto technology', 'car features', 'automotive innovations', 'car models', 'car upgrades',
        'car buying guides', 'car safety features', 'car performance tips', 'auto industry news', 'car parts and accessories', 'car repair services', 'automotive technology trends', 'car and driver reviews', 'automobile safety tips', 'car and vehicle comparisons',
        'car trends 2024', 'auto industry updates', 'car care products', 'car repair tutorials', 'car maintenance checklists', 'automotive technology updates', 'car buying advice', 'automobile safety innovations', 'car performance enhancements', 'automotive lifestyle',
        'car maintenance services', 'auto industry trends', 'car technology updates', 'car reviews and ratings', 'car safety innovations', 'car care and maintenance', 'automotive products', 'car buying trends', 'automobile reviews 2024', 'car repair solutions'
    ],
    'music.html': [
        'music', 'songs', 'albums', 'music reviews', 'music news', 'musical artists', 'music trends', 'music genres', 'music recommendations', 'music concerts',
        'music streaming', 'music industry', 'music events', 'music playlists', 'music tips', 'music and wellness', 'musical instruments', 'music for relaxation', 'music and lifestyle', 'music releases',
        'music reviews 2024', 'music and technology', 'music playlists by genre', 'musical performances', 'music industry news', 'music recommendations by genre', 'music for different moods', 'musical genres', 'music and culture', 'music events updates',
        'music streaming services', 'music for studying', 'music for working out', 'music concerts 2024', 'music festivals', 'music and mental health', 'music for relaxation and sleep', 'musical instrument reviews', 'music and art', 'music tips and advice',
        'latest music releases', 'music and wellness trends', 'music industry updates', 'musical artist profiles', 'music recommendations for special occasions', 'music and fitness', 'music reviews by artist', 'music for different activities', 'music genres and trends', 'music and entertainment',
        'music playlists for different activities', 'music industry insights', 'music and lifestyle trends', 'music event reviews', 'musical instrument trends', 'music recommendations and reviews', 'music and technology updates', 'latest musical releases', 'music news and reviews', 'music trends 2024'
    ]
}

def sanitize_filename(title):
    sanitized = re.sub(r'[<>:"/\\|?*]', '', title).strip()
    sanitized = re.sub(r'\s+', '_', sanitized)
    return sanitized

def parse_color(color_input):
    if re.match(r'^#?[0-9A-Fa-f]{6}$', color_input):
        return f'style="background-color: #{color_input.lstrip("#")};"'
    
    elif re.match(r'^rgb\(\d{1,3}, *\d{1,3}, *\d{1,3}\)$', color_input):
        return f'style="background-color: {color_input};"'
    
    elif color_input in ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'light', 'dark']:
        return f'class="bg-{color_input} text-white"'
    
    elif re.match(r'^[a-zA-Z]+$', color_input):
        return f'style="background-color: {color_input.lower()};"'
    
    else:
        return f'style="background-color: {color_input};"'

def get_page_from_description(description):
    description = description.lower()
    
    page_scores = defaultdict(int)
    
    for page, keywords in KEYWORDS.items():
        for keyword in keywords:
            page_scores[page] += description.count(keyword)
    
    if page_scores:
        best_page = max(page_scores, key=page_scores.get)
        return best_page
    return 'base.html'

def modify_template(title, header_text, primary_color, secondary_color, footer_text="&copy; 2024 Bootstrap Showcase | All rights reserved", parallax_text="Parallax Section", img1_desc="Description for Image 1", img2_desc="Description for Image 2", img3_desc="Description for Image 3", img1_link="#", img2_link="#", img3_link="#", button_text="Primary Button", button_link="#", output_path='output/generated_site.html'):
    template_path = TEMPLATES.get('base.html', 'templates/base.html')
    if not os.path.exists(template_path):
        print(Fore.RED + f"Error: Template file '{template_path}' not found." + Style.RESET_ALL)
        return

    with open(template_path, 'r') as file:
        content = file.read()

    primary_color_class = parse_color(primary_color)
    secondary_color_class = parse_color(secondary_color)

    if 'class="' in primary_color_class:
        content = content.replace('class="bg-primary text-white text-center py-4"', f'class="{primary_color_class} text-center py-4"')
    else:
        content = content.replace('class="bg-primary text-white text-center py-4"', f'class="text-center py-4" {primary_color_class}')

    if 'class="' in secondary_color_class:
        content = content.replace('class="bg-dark text-white text-center py-3"', f'class="{secondary_color_class} text-center py-3"')
    else:
        content = content.replace('class="bg-dark text-white text-center py-3"', f'class="text-center py-3" {secondary_color_class}')

    content = content.replace('<title>Bootstrap Modern Website</title>', f'<title>{title}</title>')
    content = content.replace('<h1>Bootstrap Showcase</h1>', f'<h1>{header_text}</h1>')
    content = content.replace('<h2 class="text-info">Parallax Section</h2>', f'<h2 class="text-info">{parallax_text}</h2>')
    content = content.replace('<p>Description for Image 1</p>', f'<p>{img1_desc}</p>')
    content = content.replace('<p>Description for Image 2</p>', f'<p>{img2_desc}</p>')
    content = content.replace('<p>Description for Image 3</p>', f'<p>{img3_desc}</p>')
    content = content.replace('<a href="#" class="btn btn-primary mt-3">Primary Button</a>', f'<a href="{button_link}" class="btn btn-primary mt-3">{button_text}</a>')
    content = content.replace('&copy; 2024 Bootstrap Showcase | All rights reserved', footer_text)

    content = content.replace('<img src="https://via.placeholder.com/300x200" class="img-fluid rounded mb-3" alt="Placeholder Image">', f'<img src="{img1_link}" class="img-fluid rounded mb-3" alt="Image 1">', 1)
    content = content.replace('<img src="https://via.placeholder.com/300x200" class="img-fluid rounded mb-3" alt="Placeholder Image">', f'<img src="{img2_link}" class="img-fluid rounded mb-3" alt="Image 2">', 1)
    content = content.replace('<img src="https://via.placeholder.com/300x200" class="img-fluid rounded mb-3" alt="Placeholder Image">', f'<img src="{img3_link}" class="img-fluid rounded mb-3" alt="Image 3">', 1)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as file:
        file.write(content)

    return output_path

def log_creation(description, page_type):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M")
    log_entry = (
        f"$====================@ Stijn / - / {timestamp} @====================$\n"
        f"Created a '{page_type}' page with description: '{description}'\n"
        f"$====================@ Stijn / - / {timestamp} @====================$\n\n\n"
    )
    with open("creation_log.txt", "a") as file:
        file.write(log_entry)

def ask_question(question, color=Fore.RED):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(color + question + Style.RESET_ALL)
    return input(Fore.WHITE)

def create_page():
    os.system('cls' if os.name == 'nt' else 'clear')
    mode = ask_question("Choose a mode: 'easy' or 'hard':").strip().lower()

    if mode not in ['easy', 'hard']:
        print(Fore.RED + "Invalid mode selected. Please restart the script and choose either 'easy' or 'hard'." + Style.RESET_ALL)
        return

    title = ask_question("Enter the title of the website:")
    header_text = ask_question("Enter the text for the header:")
    primary_color = ask_question("Enter the primary color (hex, rgb, or Bootstrap class):")
    secondary_color = ask_question("Enter the secondary color (hex, rgb, or Bootstrap class):")

    if mode == 'hard':
        footer_text = ask_question("Enter the footer text:")
        parallax_text = ask_question("Enter the text for the parallax section:")
        img1_desc = ask_question("Enter description for Image 1:")
        img2_desc = ask_question("Enter description for Image 2:")
        img3_desc = ask_question("Enter description for Image 3:")
        img1_link = ask_question("Enter the URL for Image 1:")
        img2_link = ask_question("Enter the URL for Image 2:")
        img3_link = ask_question("Enter the URL for Image 3:")
        button_text = ask_question("Enter the text for the primary button:")
        button_link = ask_question("Enter the URL for the primary button:")
    else:
        footer_text = "&copy; 2024 @1stijn | All rights reserved"
        parallax_text = "Parallax Section"
        img1_desc = "Description for Image 1"
        img2_desc = "Description for Image 2"
        img3_desc = "Description for Image 3"
        img1_link = "https://media.discordapp.net/attachments/1281583029894123592/1283438233841176636/fad24f9995bc7ac7b20a0e7de8e60219.jpg?ex=66e99600&is=66e84480&hm=3738fd85c56d8ab8bc5e8199a619306b1e238308fc55bc0d884d3dc0c8af949c&=&format=webp&width=1509&height=1240"
        img2_link = "https://media.discordapp.net/attachments/1281583029894123592/1283438233841176636/fad24f9995bc7ac7b20a0e7de8e60219.jpg?ex=66e99600&is=66e84480&hm=3738fd85c56d8ab8bc5e8199a619306b1e238308fc55bc0d884d3dc0c8af949c&=&format=webp&width=1509&height=1240"
        img3_link = "https://media.discordapp.net/attachments/1281583029894123592/1283438233841176636/fad24f9995bc7ac7b20a0e7de8e60219.jpg?ex=66e99600&is=66e84480&hm=3738fd85c56d8ab8bc5e8199a619306b1e238308fc55bc0d884d3dc0c8af949c&=&format=webp&width=1509&height=1240"
        button_text = "Type shi!!!!!!"
        button_link = "https://github.com/1stijn"

    description = ask_question("Describe what the website is about:")
    page = get_page_from_description(description)
    
    if page != 'base.html':
        page_type = page.split('.')[0]
        template_path = TEMPLATES.get(page, TEMPLATES['base.html'])
        sanitized_title = sanitize_filename(title)
        output_path = f'output/stijn-{sanitized_title}.html'

        created_path = modify_template(title, header_text, primary_color, secondary_color, footer_text, parallax_text, img1_desc, img2_desc, img3_desc, img1_link, img2_link, img3_link, button_text, button_link, output_path=output_path)

        if created_path:
            log_creation(description, page_type)
            os.system('cls' if os.name == 'nt' else 'clear')
            print(Fore.GREEN + f"Website created successfully at '{created_path}'." + Style.RESET_ALL)
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(Fore.RED + "There was an error creating the website." + Style.RESET_ALL)
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.YELLOW + "No matching page found." + Style.RESET_ALL)

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    create_page()