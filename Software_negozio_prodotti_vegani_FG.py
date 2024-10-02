import  json, os



def commands_list():
    
    """
    Function to show the available commands
    """
    
    print("""I comandi disponibili sono i seguenti:\n
            aggiungi: aggiungi un prodotto al magazzino \n
            elenca: elenca i prodotti in magazzino\n
            vendita: registra una vendita effettuata\n
            profitti: mostra i profitti totali\n
            aiuto: mostra i possibili comandi\n
            chiudi: esci dal programma""")
  
def get_quantity():
    """
    Function to get the value of a quantity and check that it is a positive integer number
    
    """
    while True:
        try:
            quantity = int(input("Quantità: "))
            if quantity>=0:
                break
            else:
                print("La quantità inserita deve essere un numero positivo")
        except ValueError:
            print("La quantità inserita deve essere un numero intero")
            pass
    return quantity
    
def get_price(str_input):
    """
    Function to get the value of a price and check that it is a positive integer number
    
    Input: the message to show in the input function

    """
    
    while True:
        try:
            price = float(input(str_input))
            if price>=0:
                break
            else:
                print("Il prezzo inserito deve essere un numero positivo")
            
        except ValueError:
            print("Il prezzo inserito deve essere un numero")
            pass
            
    return price

def yes_or_no():
    """
    Function to get yes/no option and check it
    """
    while True:
        ans=input("Aggiungere un altro prodotto?(si/no): ").lower()
        if ans == 'si' or ans =='no':
            break
    return ans

def get_name(str_input):
    
    """
    Function to get a string and check that there aren't spaces at the end of the input 
    """
        
    while True:
        name = input(str_input).lower()
        
        if name[-1] != ' ':
            break
        else:
            print("ATTENZIONE: non lasciare uno spazio al termine del nome del prodotto")
    return name    

        

def add_product():
    
    """
    Function to add a product   
    """
    
    add={} 
    name = get_name("Nome del prodotto: ")
    
    if 'werehouse.json' in os.listdir(): 
        with open("werehouse.json") as werehouse_json:

            werehouse_reader = json.load(werehouse_json)

            if name in werehouse_reader:
                quantity = get_quantity()
                werehouse_reader[name][0]+=quantity
                
            else:
                quantity = get_quantity()
                purchase_price = get_price("Prezzo di acquisto: ")
                sale_price = get_price("Prezzo di vendita: ")
                werehouse_reader[name]=[quantity, purchase_price, sale_price]
        
        with open("werehouse.json",'w') as werehouse_json:
            json.dump(werehouse_reader, werehouse_json,indent=6)
            
            
    else:
        quantity = get_quantity()
        purchase_price = get_price("Prezzo di acquisto: ")
        sale_price = get_price("Prezzo di vendita: ")
        
        add[name]=[quantity, purchase_price,sale_price]
        
        with open("werehouse.json",'w') as werehouse_json:
            json.dump(add, werehouse_json,indent=6)
    
    print(f"AGGIUNTO: {quantity} x {name}")

def list_products():
    """
    Function to show the content of the werehouse
    """

    if 'werehouse.json' not in os.listdir():
        print("Magazzino vuoto")
    else:
        with open("werehouse.json") as werehouse_json:
            werehouse_reader = json.load(werehouse_json)
            
            if len(werehouse_reader)==0:
                print("Magazzino vuoto")
                return
            
            print("Prodotto\tQuantità\tPrezzo")
            
            for product in werehouse_reader:
                
                print(f"{product}\t{werehouse_reader[product][0]}\t{werehouse_reader[product][2]}€\t")

def sale_products():

    """
    Function to sell products and record the sale
    """
    if 'werehouse.json' not in os.listdir():
        print("Magazzino vuoto")
        return
    else:
        sale={}
        
        name=get_name("Nome del prodotto: ")
        
        with open("werehouse.json") as werehouse_json:
            
            werehouse_reader=json.load(werehouse_json)
            
            if name not in werehouse_reader:
                print("Prodotto non presente in magazzino")
                return
            if name in werehouse_reader:
                quantity = get_quantity()
                
                if werehouse_reader[name][0] < quantity:
                    print("Quantità non sufficiente")
                    return
                sale[name]=[quantity, werehouse_reader[name][1],werehouse_reader[name][2]]
                
                
                while True:
                    continue_sale = yes_or_no()
                    if continue_sale == 'no':
                        break
                    else:
                        name=get_name("Nome del prodotto: ")
                        if name not in werehouse_reader:
                            print("Prodotto non presente in magazzino")
                            return
                        quantity = get_quantity()
                        if werehouse_reader[name][0] < quantity:
                            print("Quantità non sufficiente")
                            return
                        if name in sale:
                            sale[name][0]+=quantity
                            
                        else:
                            sale[name]=[quantity,werehouse_reader[name][1],werehouse_reader[name][2]]
                           
                for product in sale:
                    werehouse_reader[product][0]-=sale[product][0]
                    if werehouse_reader[product][0]==0:
                        del werehouse_reader[product]
                        
        with open("werehouse.json",'w') as werehouse_json:
            json.dump(werehouse_reader,werehouse_json,indent=6)
        
    
        with open("sales.txt",'a+') as sales_file:
            for product in sale:
                line = product+','+str(sale[product][0])+','+str(sale[product][1])+','+str(sale[product][2])+'\n'
                sales_file.write(line)
            
        print("VENDITA REGISTRATA")
        tot=0
        for product in sale:
            print(f"{sale[product][0]} x {product}: €{sale[product][2]}")
            tot+=sale[product][0]*sale[product][2]
        print(f"Totale: €{tot:.2f}")
            
def profits():
    
    """
    Function to calculate both gross and net profit
    """
    
    if 'sales.txt' not in os.listdir():
        print("Non è stata effettuata alcuna vendita")
    else:
        with open("sales.txt") as sales_file:
            gross_profit=0
            purchases=0
            for line in sales_file.readlines():
                gross_profit += int(line.split(',')[1])*float(line.split(',')[3][:-1])
                purchases += int(line.split(',')[1])*float(line.split(',')[2])
        
            
        return gross_profit, gross_profit-purchases




commands = ["aggiungi","elenca","profitti","vendita","aiuto","chiudi"]

while True:
    
    while True:
        instruction = input("Inserisci un comando: ").lower()
              
        if instruction in commands:
            break
        else:
            print("Comando non valido\n")
            commands_list()

    if instruction == 'aiuto':
        commands_list()
    if instruction == 'chiudi':
        
        print("A presto!")
        break
    
    if instruction == 'aggiungi':
        add_product()
        
        
    if instruction == 'elenca':
        list_products()
        
    if instruction == 'vendita':
        sale_products()
        
    if instruction.lower() == 'profitti':
        print(f"Profitto lordo: € {profits()[0]:.2f}\nProfitto netto: € {profits()[1]:.2f}")
