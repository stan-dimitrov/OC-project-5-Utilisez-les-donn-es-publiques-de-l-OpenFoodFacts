import mysql

import Database
import constants
import OpenFood

'''
db = Database.Database(constants.DB_HOST, constants.DB_PWD, constants.DB_USER, constants.DB_NAME)
db.create_db()
'''

open_food = OpenFood.OpenFood(constants.DB_HOST, constants.DB_PWD, constants.DB_USER, constants.DB_NAME)
open_food.list_categories()

user_choice = 0
while 1:
    print("\nWhich category do you want to browse?")
    id_category = int(input())
    open_food.list_foods(id_category)

    while 1:
        print("\nWhich food do you want to review the ingredients for?")
        id_food = int(input())
        food_has_substitutes = open_food.select_food(id_food)

        if food_has_substitutes == False:
            print("\nYou have chosen the food with the best nutri score in this category. Bravo!")
            print("\nThank you for using our services!")
            break

        while 1:
            print("\nDo you want us to find you a better substitute for the chosen food? (Y/N)")
            if input().lower() == "y":
                open_food.find_substitute(id_food)

                print("\nDo you want to save this substitute? (Y/N)")
                while 1:
                    if input().lower() == "y":
                        open_food.save_substitute(id_food)
                    else:
                        print("\nThank you for using our services!")
                break
            else:
                print("\nThank you for using our services!")

            break

        break

    break