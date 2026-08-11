import random
import os
from datetime import datetime
from abc import ABC, abstractmethod


LINE = "=" * 60
SMALL_LINE = "-" * 60
print(LINE)
delivery_partners = [
    "Rahul",
    "Amit",
    "Rohit",
    "Vikram",
    "Arjun",
    "Karan",
    "Mohit",
    "Aditya",
    "Sahil",
    "Ankit"
]

class Store(ABC):
    def __init__(self, store_id, name, rating, delivery_time, delivery_fee, food_type, menu,image):
        self.store_id = store_id
        self.name = name
        self.rating = rating
        self.delivery_time = delivery_time
        self.delivery_fee = delivery_fee
        self.food_type = food_type
        self.menu = menu
        self.image = image

    @abstractmethod
    def display_menu(self):
        pass

class Customer:

    def __init__(self):

        self.name = input("ENTER CUSTOMER NAME : ")
        self.phone = input("ENTER PHONE NUMBER : ")
        self.address = input("ENTER DELIVERY ADDRESS : ")

class Payment:

    def __init__(self, amount):
        self.amount = amount
        self.status = False
        self.method = None

    def make_payment(self):

        print("\n========== PAYMENT ==========")

        print("TOTAL PAYABLE :", self.amount)

        print("1. UPI")
        print("2. Card")
        print("3. Cash on Delivery")
        try:
           choice = int(input("SELECT PAYMENT METHOD : "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            return False

        if choice == 1:
            self.method = "UPI"
            self.status = True

        elif choice == 2:
            self.method = "Card"
            self.status = True

        elif choice == 3:
            self.method = "Cash on Delivery"
            self.status = True

        else:
            print("Invalid Payment Method")

        if self.status:
            print(f"Payment Successful using {self.method}")
            return True

        return False


            
class Order:

    def __init__(self,customer,store,cart):
        self.order_id = random.randint(1000,9999)
        self.customer = customer
        self.store = store
        self.cart = cart
        self.payment = None
        self.status = "Pending"
        self.delivery_partner = random.choice(delivery_partners)
        self.order_time = datetime.now()

    def display_order(self):
        if self.cart is None:
            print("ORDER CANNOT BE PLACED")
            return


        print("\n========== ORDER DETAILS ==========")

        print(f"{'ORDER ID':<20} : {self.order_id}")

        print(f"{'CUSTOMER':<20} : {self.customer.name}")

        print(f"{'PHONE':<20} : {self.customer.phone}")

        print(f"{'ADDRESS':<20} : {self.customer.address}")

        print(f"{'STORE':<20} : {self.store.name}")

        print(f"{'DELIVERY TIME':<20} : {self.store.delivery_time}")

        print(f"{'DELIVERY PARTNER':<20} : {self.delivery_partner}")

        print(f"{'ORDER TIME':<20} : {self.order_time.strftime('%d-%m-%Y %I:%M %p')}")


        print("\nYOUR BILL")
        amount = self.cart.show_cart()
        if amount == 0:
            print("ORDER CANNOT BE PLACED")
            return
        self.payment = Payment(amount)

        if self.payment.make_payment():
             print("\nPAYMENT STATUS : SUCCESFULL")
             print(f"{'PAYMENT METHOD':<20} : {self.payment.method}")
             print("\nORDER CONFIRMED")
             self.status = "Confirmed"
             print(f"{'ORDER STATUS':<20} : {self.status}")
             print(f"{'THANK YOU FOR ORDERING FROM':<20} : {self.store.name}")
             print(f"{'DELIVERY PARTNER':<20} : {self.delivery_partner}")
             print(f"{'ESTIMATED TIME':<20} : {self.store.delivery_time}")
        else:

             print("\nORDER FAILED")
    
class Cart:
    def __init__(self,store):
        self.items = []
        self.store = store

    def add_item(self, food_name,category, price,quantity):
         for item in self.items:
            if item["food"] == food_name and item["category"] == category:
                item["quantity"] += quantity
                print(f"{food_name} quantity updated.")
                return
         self.items.append({
                "food": food_name,
                "price": price,
                "quantity" : quantity,
                "category": category
            })
         print(f"{food_name} added to cart")

    def remove_item(self, item_number, quantity):

         if 1 <= item_number <= len(self.items):

             item = self.items[item_number - 1]

             if quantity <= 0:
                 print("Quantity must be greater than 0.")
                 return

             if quantity >= item["quantity"]:

                 removed_item = self.items.pop(item_number - 1)

                 print(f"{removed_item['food']} removed completely from cart.")

             else:

                 item["quantity"] -= quantity

                 print(f"{quantity} quantity removed.")
                 print(f"{ 'Remaining Quantity':<20} : {item['quantity']}")

         else:

              print("INVALID ITEM NUMBER")

    def update_item(self, item_number, quantity):

        if 1 <= item_number <= len(self.items):

            if quantity <= 0:
                print("Quantity must be greater than 0")
                return

            self.items[item_number - 1]["quantity"] = quantity
            print("Quantity Updated Successfully")

        else:
            print("INVALID ITEM NUMBER")

    def show_cart(self):

        if len(self.items) == 0:
           print("CART IS EMPTY")
           return 0

        print("\n========== YOUR CART ==========")
        total = 0
        for i, item in enumerate(self.items, 1):
            print(f"{i}. {item['food']} : ₹{item['price']} x {item['quantity']}")
            total += item['price'] * item['quantity']
        final_total = total + self.store.delivery_fee
        print(SMALL_LINE)
        print(f"{'DELIVERY FEE':<20} : {self.store.delivery_fee}")
        print(f"{'TOTAL AMOUNT':<20} : {total}")
        print(f"{'FINAL TOTAL':<20} : {final_total}")
        return final_total

class FoodRestaurant(Store):
    def display_menu(self):
        print(f"\n===== {self.name} MENU =====")

        item_number = 1
        self.food_items = {}
        for category, items in self.menu.items():
            print(f"\n==========={category}==========")
            for food, price in items.items():
                print(f"{item_number:<2}. {food:<20} : ₹{price:<10}")
                self.food_items[item_number] = {
                    "name": food,
                    "category": category,
                    "price": price,
                }
                item_number += 1
class GroceryStore(Store):
    def display_menu(self):

        print(f"\n===== {self.name} MENU =====")

        self.food_items = {}

        item_number = 1
        for category,items in self.menu.items():
            print(f"\n====={category} =====")

            for item, price in items.items():

                    print(f"{item_number:<2}. {item:<20} : ₹{price:<10}")

                    self.food_items[item_number] = {
                          "name": item,
                          "category": "Grocery",
                          "price": price
                    }
 
                    item_number += 1

class UtensilsStore(Store):
    def display_menu(self):

        print(f"\n===== {self.name} MENU =====")

        self.food_items = {}

        item_number = 1
        for category,items in self.menu.items():
            print(f"\n====={category} =====")

            for item, price in items.items():

                print(f"{item_number:<2}. {item:<20} : ₹{price:<10}")

                self.food_items[item_number] = {
                    "name": item,
                    "category": "Utensils",
                    "price": price
                }

                item_number += 1
class DeliveryApp:
    def __init__(self, stores):
        self.stores = stores

    def display_stores(self):
        print("\n===== AVAILABLE STORES =====")
        for store in self.stores:
            print(LINE)
            print(f"{'ID':<20} : {store.store_id}")
            print(f"{'Name':<20} : {store.name}")
            print(f"{'Rating':<20} : {store.rating} ⭐")
            print(f"{'Delivery Time':<20} : {store.delivery_time}")
            print(f"{'Delivery Fee':<20} : {store.delivery_fee}")
            print(f"{'Food Type':<20} : {store.food_type}")

    def choose_store(self):
        self.display_stores()
        try:
            choice = int(input("\nENTER STORE ID : "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            return None
        for store in self.stores:
            if store.store_id == choice:
                print(f"\nSTORE SELECTED : {store.name}")
                return store
        print("STORE NOT FOUND")
        return None

    
    def order_food(self, store):

          cart = Cart(store)

          while True:
               try:
                   food_choice = int(input("\nENTER FOOD ITEM NUMBER (0 TO REVIEW CART): "))
               except ValueError:
                   print("Invalid input. Please enter a number.")
                   continue

               if food_choice == 0:
                   break

               item = store.food_items.get(food_choice)

               if item:
                   try:
                    quantity = int(input("ENTER QUANTITY: "))
                   except ValueError:
                       print("Invalid input. Please enter a number.")
                       continue
                   if quantity <= 0:
                       print("Quantity must be greater than 0.")
                       continue

                   cart.add_item(
                       item["name"],
                       item["category"],
                       item["price"],
                       quantity
                   )

               else:
                    print("INVALID ITEM NUMBER")


           # Cart Review
          print("\n========== CART REVIEW ==========")

          if len(cart.items) == 0:
               print("CART IS EMPTY")
               return cart

          cart.show_cart()

          while True:
                print("\n========== CART MENU ==========")
                print("1. View Cart")
                print("2. Update Quantity")
                print("3. Remove Item")
                print("4. Continue Shopping")
                print("5. Checkout")
                print("6. Cancel Order") 
                try:
                    choice = int(input("ENTER YOUR CHOICE : "))
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue

                if choice == 1:
                    cart.show_cart()
                elif choice == 2:
                    try:
                        item_number = int(input("ENTER ITEM NUMBER TO UPDATE : "))
                        quantity = int(input("ENTER NEW QUANTITY : "))
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                        continue
                    cart.update_item(item_number, quantity)   
                elif choice == 3:
                    try:
                        item_number = int(input("ENTER ITEM NUMBER TO REMOVE : "))
                        quantity = int(input("ENTER QUANTITY TO REMOVE : "))
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                        continue
                    cart.remove_item(item_number, quantity)  

                elif choice == 4:
                    store.display_menu()
                    while True:
                        try:
                            food_choice = int(input("\nENTER FOOD ITEM NUMBER (0 TO REVIEW CART): "))
                        except ValueError:
                            print("Invalid input. Please enter a number.")
                            continue

                        if food_choice == 0:
                            break

                        item = store.food_items.get(food_choice)

                        if item:
                            try:
                                quantity = int(input("ENTER QUANTITY: "))
                            except ValueError:
                                print("Invalid input. Please enter a number.")
                                continue
                            if quantity <= 0:
                                print("Quantity must be greater than 0.")
                                continue

                            cart.add_item(
                                item["name"],
                                item["category"],
                                item["price"],
                                quantity
                            )

                        else:
                            print("INVALID ITEM NUMBER")  

                elif choice == 5:
                    print("SUCCESSFULLY CHECKED OUT")
                    return cart
                elif choice == 6:
                    print("ORDER CANCELLED")
                    print("Thank you for using our service!")
                    return None
                else:
                    print("INVALID CHOICE")
stores = [
    FoodRestaurant(
    1,
    "THE DINING REPLUBLIC",
    4.5,
    "30-40 mins",
    50,
    "Non-Veg",
    {
        "Starter": {
            "Chicken Fry": {
                "price": 200,
                "image": "chicken_fry.jpg",
                "description": "🍗 Crispy and spicy chicken pieces fried with aromatic Indian spices.",
                "bestseller": True
            },
            "Malai Chicken": {
                "price": 180,
                "image": "malai_chicken.jpg",
                "description": "🔥 Tender chicken cooked with creamy malai and rich spices.",
                "bestseller": True
            },
            "Chicken Roasted": {
                "price": 220,
                "image": "chicken_roasted.jpg",
                "description": "🍗 Juicy roasted chicken with smoky flavors and special seasoning.",
                "bestseller": False
            },
            "Fish Fry": {
                "price": 210,
                "image": "fish_fry.jpg",
                "description": "🐟 Crispy golden fish fry coated with flavorful spices.",
                "bestseller": True
            },
            "Prawns Fry": {
                "price": 200,
                "image": "prawns_fry.jpg",
                "description": "🍤 Spicy and crispy prawns fried with coastal-style spices.",
                "bestseller": False
            }
        },

        "Main Course": {
            "Chicken Biryani": {
                "price": 250,
                "image": "chicken_biryani.jpg",
                "description": "🍚 Aromatic basmati rice cooked with juicy chicken and traditional biryani spices.",
                "bestseller": True
            },
            "Mutton Biryani": {
                "price": 300,
                "image": "mutton_biryani.jpg",
                "description": "🍖 Royal biryani prepared with tender mutton and rich flavors.",
                "bestseller": True
            },
            "Butter Chicken": {
                "price": 250,
                "image": "butter_chicken.jpg",
                "description": "🔥 Creamy and buttery chicken curry with a rich tomato gravy.",
                "bestseller": True
            },
            "Chicken Afghani": {
                "price": 220,
                "image": "chicken_afghani.jpg",
                "description": "🍗 Mild and creamy Afghani chicken with delicious smoky flavors.",
                "bestseller": False
            },
            "Malai Chicken": {
                "price": 270,
                "image": "malai_chicken.jpg",
                "description": "🥘 Soft chicken pieces cooked in creamy malai sauce.",
                "bestseller": False
            },
            "Chicken Kali Mirch": {
                "price": 280,
                "image": "chicken_kali_mirch.jpg",
                "description": "🌶️ Spicy chicken curry flavored with black pepper and Indian spices.",
                "bestseller": False
            },
            "Leg Rice": {
                "price": 180,
                "image": "leg_rice.jpg",
                "description": "🍚 Flavorful rice served with delicious chicken leg pieces.",
                "bestseller": False
            },
            "Butter Naan": {
                "price": 60,
                "image": "butter_naan.jpg",
                "description": "🫓 Soft and fluffy naan topped with melted butter.",
                "bestseller": False
            },
            "Tandoori Roti": {
                "price": 40,
                "image": "tandoori_roti.jpg",
                "description": "🫓 Traditional clay oven roasted Indian bread.",
                "bestseller": False
            },
            "Salad": {
                "price": 50,
                "image": "salad.jpg",
                "description": "🥗 Fresh and healthy salad with seasonal vegetables.",
                "bestseller": False
            }
        },

        "Dessert": {
            "Shahi Tukda": {
                "price": 100,
                "image": "shahi_tukda.jpg",
                "description": "🍞 Royal dessert made with bread, milk, saffron and dry fruits.",
                "bestseller": True
            },
            "Kheer": {
                "price": 80,
                "image": "kheer.jpg",
                "description": "🍚 Traditional Indian rice pudding cooked with milk and dry fruits.",
                "bestseller": False
            },
            "Kunafa": {
                "price": 150,
                "image": "kunafa.jpg",
                "description": "🍰 Sweet Middle Eastern dessert with crispy layers and creamy filling.",
                "bestseller": True
            }
        }
    },
    "mordern1.jpg"
),
    FoodRestaurant(
        2,
        "HOUSE OF SAFFRON",
        4.6,
        "25-35 mins",
        60,
        "Veg",
        {
            "Starter": {
                "Paneer 65": {

                              "price":130,

                              "image":"paneer65.jpg",

                              "description":"Crispy spicy paneer cubes",

                              "bestseller":True

                             },
               "Chilli Paneer": { 
                              "price":130, 

                              "image":"chilli_paneer.jpg",

                              "description":"Spicy chilli paneer with vegetables",

                              "bestseller":False
                              },
 
               "Paneer Tikka": {
                             "price":200,

                             "image":"paneer_tikka.jpg",

                             "description":"Grilled paneer tikka with spices",

                             "bestseller":True
                            },

                "Veg Manchurian": {
                                 "price":180,

                                 "image":"veg_manchurian.jpg",

                                 "description":"Crispy vegetable balls with sauce",

                                 "bestseller":False
                             },
                             },
              "Main Course": {
                    "Paneer Butter Masala": {
                                             "price":250,
                                             "image":"paneer_butter_masala.jpg",
                                             "description":"Soft paneer cooked in rich buttery tomato gravy",
                                             "bestseller":True
                                                       },
    

                    "Paneer Kolhapuri": {
                                        "price":200,
                                        "image":"paneer_kolhapuri.jpg",
                                        "description":"Spicy Kolhapuri style paneer curry",
                                        "bestseller":False
                                       },


                    "Palak Paneer": {
                                    "price":300,
                                    "image":"palak_paneer.jpg",
                                    "description":"Paneer cooked with creamy spinach gravy",
                                    "bestseller":True
                                    },


                    "Paneer Kofte": {
                                   "price":180,
                                   "image":"paneer_kofte.jpg",
                                   "description":"Soft paneer kofta served with delicious gravy",
                                   "bestseller":False
                                    },


                    "Dal Tadka": { 
                                   "price":190,
                                   "image":"dal_tadka.jpg",
                                   "description":"Yellow dal tempered with Indian spices",
                                   "bestseller":False
                                },
 

                    "Mushroom Pepper Masala": {
                                    "price":180,
                                    "image":"mushroom_pepper.jpg",
                                    "description":"Spicy mushroom cooked with pepper masala",
                                    "bestseller":False
                                },


                    "Veg Kofta": {
                                    "price":190,
                                    "image":"veg_kofta.jpg",
                                    "description":"Vegetable kofta with rich curry",
                                    "bestseller":False
                                 },


                    "Kadai Veg Curry": {
                                    "price":160,
                                    "image":"kadai_veg.jpg",
                                    "description":"Mixed vegetables cooked in kadai masala",
                                    "bestseller":False
                                  }

                    },  
              "Dessert": {
                     "Gulab Jamun": {
                                     "price":40,
                                     "image":"gulab_jamun.jpg",
                                     "description":"Soft and sweet gulab jamun soaked in sugar syrup",
                                     "bestseller":True
                                    },


                     "Falooda": {
                                    "price":100,
                                    "image":"falooda.jpg",
                                    "description":"Refreshing falooda with milk, jelly and ice cream",
                                    "bestseller":False
                                },


                     "Kesar Falooda": {
                                    "price":150,
                                    "image":"kesar_falooda.jpg",
                                    "description":"Royal falooda with saffron flavour and ice cream",
                                    "bestseller":True
                                },


                     "Chocolate Scoop": {
                                        "price":60,
                                        "image":"chocolate_scoop.jpg",
                                        "description":"Rich chocolate ice cream scoop",
                                        "bestseller":False
                                        },


                     "Nut Sundae": {
                                        "price":80,
                                        "image":"nut_sundae.jpg",
                                        "description":"Creamy sundae topped with crunchy nuts",
                                        "bestseller":False
                                   }

                        },
                      },
                          "mordern2.jpg"
               ),
    FoodRestaurant(
    3,
    "THE CULINARY CROWN",
    4.9,
    "35-45 mins",
    70,
    "Hybrid",
    {
        "Veg Starter": {
            "Paneer Tikka": {
                "price": 220,
                "image": "paneer_tikka.jpg",
                "description": "🌶️ Packed with bold Indian spices and smoky flavors.",
                "bestseller": True
            },
            "Veg Spring Roll": {
                "price": 180,
                "image": "veg_spring_roll.jpg",
                "description": "🥢 Crispy on the outside and flavorful on the inside.",
                "bestseller": False
            },
            "Hara Bhara Kabab": {
                "price": 190,
                "image": "hara_bhara_kabab.jpg",
                "description": "🌿 A healthy and delicious vegetarian party starter.",
                "bestseller": False
            },
            "Crispy Corn": {
                "price": 170,
                "image": "crispy_corn.jpg",
                "description": "🌶️ Sweet, crispy and packed with spicy flavors.",
                "bestseller": True
            }
        },

        "Non-Veg Starter": {
            "Chicken Tikka": {
                "price": 280,
                "image": "chicken_tikka.jpg",
                "description": "🔥 Juicy chicken pieces marinated with aromatic spices and grilled to perfection.",
                "bestseller": True
            },
            "Chicken Lollipop": {
                "price": 260,
                "image": "chicken_lollipop.jpg",
                "description": "🍗 Crispy chicken wings with a spicy and flavorful coating.",
                "bestseller": False
            },
            "Tandoori Chicken": {
                "price": 350,
                "image": "tandoori_chicken.jpg",
                "description": "🔥 Classic smoky tandoori chicken cooked with rich Indian spices.",
                "bestseller": True
            },
            "Fish Fingers": {
                "price": 300,
                "image": "fish_fingers.jpg",
                "description": "🐟 Crispy golden fish strips served as a perfect appetizer.",
                "bestseller": False
            }
        },

        "Veg Main Course": {
            "Paneer Butter Masala": {
                "price": 260,
                "image": "paneer_butter_masala.jpg",
                "description": "🧀 Soft paneer cooked in a rich and creamy tomato-based gravy.",
                "bestseller": True
            },
            "Kadai Paneer": {
                "price": 240,
                "image": "kadai_paneer.jpg",
                "description": "🌶️ Spicy paneer cooked with capsicum and traditional Indian spices.",
                "bestseller": False
            },
            "Dal Makhani": {
                "price": 210,
                "image": "dal_makhani.jpg",
                "description": "🥣 Creamy black lentils slow-cooked with butter and spices.",
                "bestseller": False
            },
            "Veg Biryani": {
                "price": 220,
                "image": "veg_biryani.jpg",
                "description": "🍚 Aromatic rice cooked with vegetables and flavorful spices.",
                "bestseller": True
            },
            "Butter Naan": {
                "price": 60,
                "image": "butter_naan.jpg",
                "description": "🫓 Soft and fluffy Indian bread topped with butter.",
                "bestseller": False
            },
            "Jeera Rice": {
                "price": 150,
                "image": "jeera_rice.jpg",
                "description": "🍚 Fragrant basmati rice flavored with cumin seeds.",
                "bestseller": False
            }
        },

        "Non-Veg Main Course": {
            "Chicken Biryani": {
                "price": 280,
                "image": "chicken_biryani.jpg",
                "description": "🍗 Flavorful basmati rice cooked with spicy chicken and aromatic spices.",
                "bestseller": True
            },
            "Mutton Biryani": {
                "price": 350,
                "image": "mutton_biryani.jpg",
                "description": "🍖 Royal biryani made with tender mutton and rich spices.",
                "bestseller": True
            },
            "Butter Chicken": {
                "price": 320,
                "image": "butter_chicken.jpg",
                "description": "🔥 Creamy and buttery chicken curry with rich flavors.",
                "bestseller": True
            },
            "Chicken Curry": {
                "price": 290,
                "image": "chicken_curry.jpg",
                "description": "🍗 Traditional spicy chicken curry cooked with Indian spices.",
                "bestseller": False
            },
            "Mutton Rogan Josh": {
                "price": 380,
                "image": "mutton_rogan_josh.jpg",
                "description": "🍖 Slow-cooked mutton curry with aromatic Kashmiri spices.",
                "bestseller": False
            },
            "Butter Naan": {
                "price": 60,
                "image": "butter_naan.jpg",
                "description": "🫓 Soft naan topped with melted butter.",
                "bestseller": False
            }
        },

        "Milkshakes": {
            "Chocolate Milkshake": {
                "price": 140,
                "image": "chocolate_milkshake.jpg",
                "description": "🥤 Rich and creamy chocolate flavored milkshake.",
                "bestseller": True
            },
            "Oreo Milkshake": {
                "price": 160,
                "image": "oreo_milkshake.jpg",
                "description": "🍪 Creamy milkshake blended with Oreo cookies.",
                "bestseller": True
            },
            "KitKat Milkshake": {
                "price": 170,
                "image": "kitkat_milkshake.jpg",
                "description": "🍫 Delicious shake with crunchy KitKat flavor.",
                "bestseller": False
            },
            "Strawberry Milkshake": {
                "price": 150,
                "image": "strawberry_milkshake.jpg",
                "description": "🍓 Fresh and creamy strawberry flavored shake.",
                "bestseller": False
            },
            "Mango Milkshake": {
                "price": 140,
                "image": "mango_milkshake.jpg",
                "description": "🥭 Refreshing mango shake made with fresh mangoes.",
                "bestseller": True
            },
            "Cold Coffee": {
                "price": 130,
                "image": "cold_coffee.jpg",
                "description": "☕ Chilled coffee blended with milk and ice cream.",
                "bestseller": False
            }
        },

        "Dessert": {
            "Brownie with Ice Cream": {
                "price": 180,
                "image": "brownie_icecream.jpg",
                "description": "🍫 Warm brownie served with a scoop of creamy ice cream.",
                "bestseller": True
            },
            "Chocolate Lava Cake": {
                "price": 170,
                "image": "chocolate_lava_cake.jpg",
                "description": "🍰 Soft chocolate cake with a rich molten center.",
                "bestseller": True
            },
            "Gulab Jamun": {
                "price": 80,
                "image": "gulab_jamun.jpg",
                "description": "🍯 Soft sweet dumplings soaked in sugar syrup.",
                "bestseller": False
            },
            "Ice Cream Sundae": {
                "price": 150,
                "image": "icecream_sundae.jpg",
                "description": "🍨 Delicious ice cream topped with chocolate and nuts.",
                "bestseller": False
            },
            "Cheesecake": {
                "price": 220,
                "image": "cheesecake.jpg",
                "description": "🍰 Creamy cheesecake with a rich and smooth texture.",
                "bestseller": False
            }
        }
    },
    "mordern3.jpg"
),
]
grocery1 = GroceryStore(
    101,
    "Fresh Mart Grocery",
    4.5,
    "30 min",
    20,
    "Grocery",
    {
        "Groceries": {
            "Rice 5kg": {
                "price": 350,
                "image": "rice.jpg",
                "description": "🍚 Premium quality rice perfect for daily meals.",
                "bestseller": True
            },
            "Wheat Flour 5kg": {
                "price": 250,
                "image": "wheat_flour.jpg",
                "description": "🌾 Fresh and finely ground wheat flour for soft rotis.",
                "bestseller": True
            },
            "Sugar 1kg": {
                "price": 50,
                "image": "sugar.jpg",
                "description": "🍬 High quality refined sugar for everyday use.",
                "bestseller": False
            },
            "Salt 1kg": {
                "price": 25,
                "image": "salt.jpg",
                "description": "🧂 Pure iodized salt for cooking and seasoning.",
                "bestseller": False
            },
            "Cooking Oil 1L": {
                "price": 150,
                "image": "cooking_oil.jpg",
                "description": "🛢️ Healthy cooking oil suitable for frying and cooking.",
                "bestseller": True
            },
            "Milk 1L": {
                "price": 60,
                "image": "milk.jpg",
                "description": "🥛 Fresh and nutritious milk for everyday consumption.",
                "bestseller": True
            },
            "Bread": {
                "price": 40,
                "image": "bread.jpg",
                "description": "🍞 Soft and fresh bread perfect for breakfast.",
                "bestseller": False
            },
            "Eggs (12 pcs)": {
                "price": 80,
                "image": "eggs.jpg",
                "description": "🥚 Fresh eggs rich in protein and nutrition.",
                "bestseller": True
            },
            "Tea Powder 500g": {
                "price": 220,
                "image": "tea_powder.jpg",
                "description": "☕ Aromatic tea powder for a refreshing cup of tea.",
                "bestseller": False
            },
            "Coffee 200g": {
                "price": 180,
                "image": "coffee.jpg",
                "description": "☕ Rich coffee powder with strong aroma and flavor.",
                "bestseller": False
            },
            "Biscuits Pack": {
                "price": 30,
                "image": "biscuits.jpg",
                "description": "🍪 Crunchy and tasty biscuits for snacks.",
                "bestseller": False
            },
            "Maggi Noodles": {
                "price": 15,
                "image": "maggi.jpg",
                "description": "🍜 Quick and delicious instant noodles.",
                "bestseller": True
            },
            "Pasta 500g": {
                "price": 90,
                "image": "pasta.jpg",
                "description": "🍝 Premium pasta for delicious homemade recipes.",
                "bestseller": False
            },
            "Corn Flakes": {
                "price": 180,
                "image": "corn_flakes.jpg",
                "description": "🥣 Healthy breakfast cereal with great taste.",
                "bestseller": False
            },
            "Dry Fruits 250g": {
                "price": 300,
                "image": "dry_fruits.jpg",
                "description": "🥜 Premium dry fruits packed with nutrients.",
                "bestseller": True
            },
            "Detergent Powder 1kg": {
                "price": 120,
                "image": "detergent.jpg",
                "description": "🧺 Powerful detergent for clean and fresh clothes.",
                "bestseller": False
            },
            "Dishwash Bar": {
                "price": 25,
                "image": "dishwash_bar.jpg",
                "description": "🧽 Removes grease and keeps utensils clean.",
                "bestseller": False
            },
            "Shampoo Bottle": {
                "price": 150,
                "image": "shampoo.jpg",
                "description": "🧴 Gentle shampoo for healthy and clean hair.",
                "bestseller": False
            },
            "Toothpaste": {
                "price": 90,
                "image": "toothpaste.jpg",
                "description": "🪥 Daily dental care toothpaste for fresh breath.",
                "bestseller": True
            },
            "Hand Wash": {
                "price": 100,
                "image": "handwash.jpg",
                "description": "🧴 Liquid hand wash for clean and protected hands.",
                "bestseller": False
            }
        }
    },
    "mordern6.jpg"
)


utensils1 = UtensilsStore(
    102,
    "Home Essentials",
    4.3,
    "45 min",
    30,
    "Utensils",
    {
        "Utensils": {
            "Steel Plate": {
                "price": 120,
                "image": "steel_plate.jpg",
                "description": "🍽️ Durable stainless steel plate perfect for everyday meals.",
                "bestseller": True
            },
            "Steel Glass": {
                "price": 80,
                "image": "steel_glass.jpg",
                "description": "🥛 Strong and reusable stainless steel drinking glass.",
                "bestseller": False
            },
            "Steel Bowl": {
                "price": 60,
                "image": "steel_bowl.jpg",
                "description": "🥣 High-quality steel bowl for serving food.",
                "bestseller": False
            },
            "Spoon Set (6 pcs)": {
                "price": 150,
                "image": "spoon_set.jpg",
                "description": "🥄 Premium spoon set suitable for daily dining.",
                "bestseller": True
            },
            "Fork Set (6 pcs)": {
                "price": 180,
                "image": "fork_set.jpg",
                "description": "🍴 Elegant fork set for comfortable dining.",
                "bestseller": False
            },
            "Knife Set": {
                "price": 500,
                "image": "knife_set.jpg",
                "description": "🔪 Sharp and durable kitchen knife set.",
                "bestseller": False
            },
            "Dinner Set": {
                "price": 1200,
                "image": "dinner_set.jpg",
                "description": "🍽️ Complete dinner set for family dining.",
                "bestseller": True
            },
            "Pressure Cooker 5L": {
                "price": 900,
                "image": "pressure_cooker.jpg",
                "description": "🍲 Strong pressure cooker for fast and efficient cooking.",
                "bestseller": True
            },
            "Non Stick Pan": {
                "price": 700,
                "image": "non_stick_pan.jpg",
                "description": "🍳 Non-stick pan for healthy and easy cooking.",
                "bestseller": True
            },
            "Kadai": {
                "price": 600,
                "image": "kadai.jpg",
                "description": "🥘 Traditional kadai for frying and cooking dishes.",
                "bestseller": False
            },
            "Frying Pan": {
                "price": 550,
                "image": "frying_pan.jpg",
                "description": "🍳 Quality frying pan for everyday cooking.",
                "bestseller": False
            },
            "Water Bottle": {
                "price": 250,
                "image": "water_bottle.jpg",
                "description": "💧 Durable water bottle for home and travel use.",
                "bestseller": False
            },
            "Lunch Box": {
                "price": 350,
                "image": "lunch_box.jpg",
                "description": "🍱 Leak-proof lunch box for carrying meals.",
                "bestseller": True
            },
            "Tea Cup Set": {
                "price": 400,
                "image": "tea_cup_set.jpg",
                "description": "☕ Beautiful tea cup set for serving beverages.",
                "bestseller": False
            },
            "Coffee Mug": {
                "price": 150,
                "image": "coffee_mug.jpg",
                "description": "☕ Stylish coffee mug for your daily drinks.",
                "bestseller": False
            },
            "Chopping Board": {
                "price": 200,
                "image": "chopping_board.jpg",
                "description": "🔪 Strong chopping board for kitchen preparation.",
                "bestseller": False
            },
            "Gas Lighter": {
                "price": 100,
                "image": "gas_lighter.jpg",
                "description": "🔥 Safe and easy-to-use gas stove lighter.",
                "bestseller": False
            },
            "Storage Container Set": {
                "price": 800,
                "image": "storage_container.jpg",
                "description": "📦 Airtight containers to keep food fresh and organized.",
                "bestseller": True
            },
            "Rolling Pin": {
                "price": 120,
                "image": "rolling_pin.jpg",
                "description": "🫓 Wooden rolling pin for making rotis and chapatis.",
                "bestseller": False
            },
            "Tawa": {
                "price": 450,
                "image": "tawa.jpg",
                "description": "🥞 Flat cooking tawa for making rotis and pancakes.",
                "bestseller": True
            }
        }
    },
    "mordern7.jpg"
)





stores.append(grocery1)
stores.append(utensils1)