from django.core.management.base import BaseCommand
from retail_management.apps.inventory.models import Category, Product
import random
from decimal import Decimal
import itertools

class Command(BaseCommand):
    help = 'Deletes all products and categories, then generates new products with simple names and specified categories.'

    def handle(self, *args, **kwargs):
        # Delete all existing products and categories
        self.stdout.write('Deleting existing products and categories...')
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Define categories
        categories = [
            'Electronics',
            'Furniture',
            'Home Appliances',
            'Drugs',
            'Construction Materials',
            'Clothes',
            'Grocery Items',
            'Toys',
            'Books',
            'Sports Equipment',
            'Office Supplies',
            'Beauty Products',
            'Pet Supplies',
            'Garden Tools',
            'Automotive Parts',
        ]

        # Example product names for each category
        product_names = {
            'Electronics': [
                'Smartphone', 'Tablet', 'Laptop', 'Desktop Computer', 'Smartwatch',
                'Bluetooth Speaker', 'Headphones', 'Digital Camera', 'Monitor', 'Printer',
                'Router', 'USB Drive', 'External Hard Drive', 'Projector', 'VR Headset',
                'E-Reader', 'Webcam', 'Microphone', 'Graphics Tablet', 'Game Controller',
                'Wireless Earbuds', 'Power Bank', 'Smart TV', 'Media Player', 'Keyboard',
                'Mouse', 'Scanner', 'Fitness Tracker', 'GPS Device', 'Drone',
                'Security Camera', 'Portable Speaker', 'Audio Receiver', 'Gaming Console', 'Network Switch',
                'Wireless Charger', 'Memory Card', 'Barcode Scanner', 'Digital Voice Recorder', 'Streaming Device',
                'Portable Monitor', 'Surge Protector', 'Uninterruptible Power Supply', 'Desk Lamp', 'Cooling Pad',
            ],
            'Furniture': [
                'Sofa', 'Dining Table', 'Office Chair', 'Bookshelf', 'Bed Frame',
                'Wardrobe', 'Coffee Table', 'TV Stand', 'Recliner', 'Nightstand',
                'Dresser', 'Bar Stool', 'Shoe Rack', 'Folding Table', 'Rocking Chair',
                'Chest of Drawers', 'Bench', 'Ottoman', 'Desk', 'Armchair',
                'Corner Sofa', 'Sectional Sofa', 'Bunk Bed', 'Futon', 'Daybed',
                'Console Table', 'Side Table', 'Dining Chair', 'Kitchen Island', 'Buffet Cabinet',
                'China Cabinet', 'Curio Cabinet', 'Filing Cabinet', 'Storage Cabinet', 'Bathroom Vanity',
                'Coat Rack', 'Room Divider', 'Bean Bag', 'Hammock', 'Patio Chair',
                'Patio Table', 'Garden Bench', 'Adirondack Chair', 'Swing Chair', 'Stool',
            ],
            'Home Appliances': [
                'Refrigerator', 'Washing Machine', 'Microwave Oven', 'Air Conditioner', 'Vacuum Cleaner',
                'Dishwasher', 'Water Purifier', 'Electric Kettle', 'Toaster', 'Blender',
                'Food Processor', 'Rice Cooker', 'Heater', 'Ceiling Fan', 'Iron',
                'Juicer', 'Induction Cooktop', 'Geyser', 'Chimney', 'Sewing Machine',
                'Air Fryer', 'Coffee Maker', 'Mixer Grinder', 'Hand Mixer', 'Sandwich Maker',
                'Waffle Maker', 'Slow Cooker', 'Pressure Cooker', 'Electric Grill', 'Deep Fryer',
                'Bread Maker', 'Ice Cream Maker', 'Yogurt Maker', 'Egg Boiler', 'Popcorn Maker',
                'Electric Steamer', 'Dehumidifier', 'Air Purifier', 'Clothes Dryer', 'Garment Steamer',
                'Hair Dryer', 'Electric Shaver', 'Electric Toothbrush', 'Water Heater', 'Exhaust Fan',
            ],
            'Drugs': [
                'Paracetamol Tablets', 'Ibuprofen Capsules', 'Cough Syrup', 'Antacid Suspension', 'Vitamin C Tablets',
                'Antibiotic Ointment', 'Allergy Relief Tablets', 'Pain Relief Gel', 'Antiseptic Solution', 'Eye Drops',
                'Nasal Spray', 'Multivitamin Syrup', 'Antifungal Cream', 'Digestive Enzyme Tablets', 'Calcium Tablets',
                'Iron Supplement', 'Antihistamine Tablets', 'Electrolyte Powder', 'Laxative Syrup', 'Antimalarial Tablets',
                'Vitamin D Tablets', 'Vitamin B Complex', 'Zinc Tablets', 'Magnesium Supplements', 'Omega-3 Capsules',
                'Protein Powder', 'Herbal Cough Drops', 'Throat Lozenges', 'Muscle Relaxant Gel', 'Burn Ointment',
                'Wound Dressing', 'Bandage Roll', 'Adhesive Bandages', 'Gauze Pads', 'Medical Tape',
                'Thermometer', 'Blood Pressure Monitor', 'Glucose Test Strips', 'Pregnancy Test Kit', 'First Aid Kit',
                'Cold Compress', 'Hot Water Bottle', 'Heating Pad', 'Pill Organizer', 'Medicine Dropper',
            ],
            'Construction Materials': [
                'Cement Bag', 'Red Bricks', 'Steel Rods', 'Sand (50kg)', 'Gravel (25kg)',
                'Plywood Sheet', 'PVC Pipes', 'Ceramic Tiles', 'Paint Bucket', 'Glass Panel',
                'Roofing Sheet', 'Concrete Blocks', 'Insulation Roll', 'Adhesive', 'Door Frame',
                'Window Frame', 'Marble Slab', 'Granite Tile', 'Wire Mesh', 'Wall Putty',
                'Wooden Planks', 'Laminate Flooring', 'Vinyl Flooring', 'Carpet Roll', 'Hardwood Flooring',
                'Drywall Sheet', 'Ceiling Tiles', 'Roof Tiles', 'Gypsum Board', 'Fiber Cement Board',
                'Aluminum Sheets', 'Copper Pipes', 'Brass Fittings', 'Stainless Steel Mesh', 'Galvanized Sheet',
                'Electrical Conduit', 'Junction Box', 'Circuit Breaker', 'Electrical Wire Roll', 'Power Socket',
                'Light Switch', 'Door Handle', 'Door Hinges', 'Door Lock', 'Window Glass',
            ],
            'Clothes': [
                'T-Shirt', 'Jeans', 'Jacket', 'Sweater', 'Dress',
                'Shorts', 'Skirt', 'Blazer', 'Shirt', 'Polo Shirt',
                'Track Pants', 'Hoodie', 'Socks', 'Scarf', 'Cap',
                'Leggings', 'Kurta', 'Dupatta', 'Suit', 'Raincoat',
                'Formal Trousers', 'Cargo Pants', 'Denim Shirt', 'Formal Shirt', 'Casual Shirt',
                'Winter Coat', 'Cardigan', 'Vest', 'Sweatshirt', 'Tank Top',
                'Pajamas', 'Nightgown', 'Bathrobe', 'Swimsuit', 'Bikini',
                'Gloves', 'Beanie', 'Sun Hat', 'Belt', 'Tie',
                'Bow Tie', 'Suspenders', 'Handkerchief', 'Shawl', 'Stole',
            ],
            'Grocery Items': [
                'Basmati Rice (1kg)', 'Wheat Flour (1kg)', 'Sugar (1kg)', 'Salt (1kg)', 'Cooking Oil (1L)',
                'Toor Dal (1kg)', 'Chana Dal (1kg)', 'Moong Dal (1kg)', 'Tea Powder (500g)', 'Coffee Powder (250g)',
                'Milk Powder (500g)', 'Cornflakes (500g)', 'Oats (1kg)', 'Honey (250g)', 'Peanut Butter (500g)',
                'Jam (250g)', 'Tomato Ketchup (500g)', 'Pickle (200g)', 'Ghee (500g)', 'Paneer (200g)',
                'Brown Rice (1kg)', 'Quinoa (500g)', 'Pasta (500g)', 'Noodles (200g)', 'Soy Sauce (200ml)',
                'Vinegar (250ml)', 'Olive Oil (500ml)', 'Mustard Oil (500ml)', 'Coconut Oil (250ml)', 'Semolina (500g)',
                'Poha (500g)', 'Vermicelli (500g)', 'Baking Powder (100g)', 'Baking Soda (100g)', 'Yeast (100g)',
                'Cocoa Powder (200g)', 'Custard Powder (100g)', 'Jelly Crystals (100g)', 'Condensed Milk (400g)', 'Dried Fruits (200g)',
                'Nuts Mix (250g)', 'Spice Mix (100g)', 'Turmeric Powder (100g)', 'Chili Powder (100g)', 'Coriander Powder (100g)',
            ],
            'Toys': [
                'Building Blocks', 'Remote Control Car', 'Doll', 'Puzzle Set', 'Action Figure',
                'Board Game', 'Toy Train', "Rubik's Cube", 'Yo-Yo', 'Kite',
                'Plush Bear', 'Toy Drum', 'Jump Rope', 'Water Gun', 'Toy Helicopter',
                'Marbles', 'Spinning Top', 'Toy Boat', 'Bubble Maker', 'Toy Phone',
                'Toy Kitchen Set', 'Toy Tool Set', 'Toy Medical Kit', 'Toy Cash Register', 'Play Tent',
                'Toy Sword', 'Toy Shield', 'Toy Bow and Arrow', 'Toy Binoculars', 'Toy Telescope',
                'Toy Microscope', 'Science Kit', 'Art Set', 'Clay Modeling Set', 'Coloring Book',
                'Toy Piano', 'Toy Guitar', 'Toy Xylophone', 'Toy Drum Set', 'Bubble Machine',
                'Toy Robot', 'Toy Dinosaur', 'Toy Farm Animals', 'Toy Wild Animals', 'Toy Insects',
            ],
            'Books': [
                'Science Fiction Novel', 'Mystery Thriller', 'Cookbook', "Children's Storybook", 'Biography',
                'Self-Help Guide', 'Travelogue', 'Poetry Collection', 'Graphic Novel', 'Classic Literature',
                'History Book', 'Language Textbook', 'Math Workbook', 'Art Album', 'Encyclopedia',
                'Fantasy Adventure', 'Romance Novel', 'Horror Story', 'Business Handbook', 'Health Guide',
                'Philosophy Book', 'Psychology Textbook', 'Physics Textbook', 'Chemistry Textbook', 'Biology Textbook',
                'Computer Programming Guide', 'Web Design Book', 'Photography Guide', 'Drawing Manual', 'Painting Tutorial',
                'Gardening Guide', 'Home Decoration Book', 'DIY Project Book', 'Craft Ideas Book', 'Knitting Pattern Book',
                'Mythology Collection', 'Historical Fiction', 'Young Adult Novel', 'Short Story Collection', 'Essay Collection',
                'Dictionary', 'Thesaurus', 'Atlas', 'Almanac', 'Journal',
            ],
            'Sports Equipment': [
                'Football', 'Cricket Bat', 'Badminton Racket', 'Tennis Ball', 'Basketball',
                'Skipping Rope', 'Yoga Mat', 'Dumbbells', 'Table Tennis Bat', 'Hockey Stick',
                'Golf Ball', 'Boxing Gloves', 'Swimming Goggles', 'Baseball Cap', 'Cycling Helmet',
                'Volleyball', 'Shuttlecock', 'Roller Skates', 'Surfboard', 'Ski Poles',
            ],
            'Office Supplies': [
                'Notebook', 'Ballpoint Pen', 'Pencil Set', 'Stapler', 'Paper Clips',
                'Sticky Notes', 'Highlighter', 'Marker Set', 'Scissors', 'Tape Dispenser',
                'Desk Organizer', 'File Folder', 'Document Tray', 'Binder Clips', 'Rubber Bands',
                'Calculator', 'Desk Calendar', 'Whiteboard', 'Whiteboard Marker', 'Eraser',
            ],
            'Beauty Products': [
                'Shampoo', 'Conditioner', 'Body Wash', 'Face Wash', 'Moisturizer',
                'Sunscreen', 'Face Mask', 'Hair Serum', 'Body Lotion', 'Lip Balm',
                'Facial Toner', 'Exfoliating Scrub', 'Hair Oil', 'Shower Gel', 'Deodorant',
                'Hair Spray', 'Nail Polish', 'Makeup Remover', 'Hand Cream', 'Foot Cream',
            ],
            'Pet Supplies': [
                'Dog Food', 'Cat Food', 'Pet Bowl', 'Pet Bed', 'Pet Collar',
                'Pet Leash', 'Pet Toy', 'Pet Shampoo', 'Pet Brush', 'Pet Carrier',
                'Fish Food', 'Bird Seed', 'Pet Cage', 'Pet Treats', 'Pet Medicine',
                'Pet Litter Box', 'Pet Litter', 'Pet Nail Clipper', 'Pet Clothes', 'Pet Feeding Bottle',
            ],
            'Garden Tools': [
                'Garden Shovel', 'Garden Rake', 'Pruning Shears', 'Watering Can', 'Garden Hose',
                'Garden Gloves', 'Trowel', 'Garden Fork', 'Hedge Trimmer', 'Lawn Mower',
                'Grass Trimmer', 'Wheelbarrow', 'Garden Sprayer', 'Weed Remover', 'Garden Scissors',
                'Plant Pot', 'Potting Soil', 'Plant Seeds', 'Plant Fertilizer', 'Garden Netting',
            ],
            'Automotive Parts': [
                'Car Battery', 'Windshield Wiper', 'Air Filter', 'Oil Filter', 'Spark Plug',
                'Brake Pad', 'Headlight Bulb', 'Car Fuse', 'Radiator Cap', 'Tire Pressure Gauge',
                'Car Jack', 'Jumper Cable', 'Car Polish', 'Car Shampoo', 'Car Vacuum Cleaner',
                'Car Floor Mat', 'Car Seat Cover', 'Car Air Freshener', 'Car Phone Holder', 'Car Charger',
            ],
        }

        for cat in categories:
            category = Category.objects.create(name=cat, description=f'{cat} category')
            for pname in product_names[cat]:
                price = Decimal(random.uniform(10, 2000)).quantize(Decimal('0.01'))
                Product.objects.create(
                    name=pname,
                    description=f'{pname} in {cat.lower()}',
                    category=category,
                    price=price,
                    stock_quantity=random.randint(10, 100),
                    reorder_level=random.randint(5, 20)
                )
        self.stdout.write(self.style.SUCCESS('All products and categories replaced with new, simple items.')) 