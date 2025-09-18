# add_product.py
import os
from supabase import create_client, Client 
from dotenv import load_dotenv 
 
load_dotenv()
 
url = os.getenv("supabase_url")
key = os.getenv("supabase_anon_key")
sb: Client = create_client(url, key)
 
def add_book(title, author, category, stock):
    payload = {"title": title, "author": author, "category": category, "stock": stock}
    resp = sb.table("books").insert(payload).execute()
    return resp.data

def add_member(name,email):
    payload = {"name": name, "email": email}
    resp = sb.table("members").insert(payload).execute()
    return resp.data
 
def list_books():
    resp = sb.table("books").select("*").order("book_id", desc=False).execute()
    return resp.data

def search_title(title):
    
    resp = sb.table("books").select("*").like("title", f"%{title}%").execute()
    return resp.data

def search_author(author):
    
    resp = sb.table("books").select("*").like("author", f"%{author}%").execute()
    return resp.data

def search_category(category):
    
    resp = sb.table("books").select("*").like("category", f"%{category}%").execute()
    return resp.data

def search_member(member_id):
    
    resp = sb.table("members").select("*").eq("member_id", f"{member_id}").execute()
    return resp.data

def update_stock(book_id, new_stock):
    resp = sb.table("books").update({"stock": new_stock}).eq("book_id", book_id).execute()
    return resp.data

def update_member(member_id, new_mail):
    resp = sb.table("members").update({"email": new_mail}).eq("member_id", member_id).execute()
    return resp.data

def delete_book(book_id):
    try:
        resp = sb.table("books").delete().eq("book_id", book_id).execute()
        if not resp.data:  
            return {"error": f"Cannot delete book {book_id}, it may be borrowed or not exist."}
        return {"success": f"Book {book_id} deleted successfully."}
    except Exception as e:
        if "violates foreign key constraint" in str(e):
            return {"error": f" Cannot delete book {book_id}, the book is still have in borrow records."}
        return {"error": str(e)}



def delete_member(member_id):
    try:
        resp = sb.table("members").delete().eq("member_id", member_id).execute()
        if not resp.data:
            return {"error": f" Cannot delete member {member_id}, they may have borrowed books or not exist."}
        return {"success": f" Member {member_id} deleted successfully."}
    except Exception as e:
        if "violates foreign key constraint" in str(e):
            return {"error": f" Cannot delete member {member_id}, they still have borrow records."}
        return {"error": str(e)}





if __name__ == "__main__":
    while(True):
        print("enter the operations to perform:\n1.add member\n2.add book\n3.List books\n4.search book\n5.search member\n6.update stock\n7.update member\n8.delete member\n9.delete book\n10.exit")
        ch=int(input("enter your choice:"))
        if ch==1:
            name = input("Enter name: ").strip()
            email = input("Enter email: ").strip()
            
 
            created = add_member(name,email)
            print("Inserted:", created)

        elif ch==2:
            title = input("Enter book title: ").strip()
            author = input("Enter author name: ").strip()
            category = (input("Enter category: ").strip())
            stock = int(input("Enter stock: ").strip())
 
            created = add_book(title, author, category, stock)
            print("Inserted:", created)

        elif ch==3:
            products = list_books()
            if products:
                print("Products:")
                for p in products:
                    print(f"{p['book_id']}: {p['title']} (author:{p['author']}) — category: {p['category']} — stock: {p['stock']}")
            else:
                print("No books found.")
        elif ch==4:
            key=int(input("enter your choice of searching\n1.title\n2.author\n3.category:"))
            if key==1:
                search=input("enter title:")
                books=search_title(search)
                if books:
                    print("Books:")
                    for book in books:
                        print(f"{book['book_id']}: {book['title']} (author:{book['author']}) — category: {book['category']} — stock: {book['stock']}")
                else:
                    print("No books found.")

            elif key==2:
                search=input("enter author:")
                books=search_author(search)
                if books:
                    print("Books:")
                    for book in books:
                        print(f"{book['book_id']}: {book['title']} (author:{book['author']}) — category: {book['category']} — stock: {book['stock']}")
                else:
                    print("No books found.")

            elif key==3:
                search=input("enter category:")
                books=search_category(search)
                if books:
                    print("Books:")
                    for book in books:
                        print(f"{book['book_id']}: {book['title']} (author:{book['author']}) — category: {book['category']} — stock: {book['stock']}")
                else:
                    print("No books found.")

        elif ch==5:
            search=input("enter member_id:")
            member=search_member(search)
            if member:
                print("member details:")
                for m in member:
                        print(f"{m['member_id']}: {m['name']} (email:{m['email']}) ")
            else:
                print("No such member found.")

        elif ch==6:
            book_id = int(input("Enter book_id to update: ").strip())
            new_stock = int(input("Enter new stock value: ").strip())
 
            updated = update_stock(book_id, new_stock)
            if updated:
                print("Updated record:", updated)
            else:
                print("No record updated — check book_id.")

        elif ch==7:
            member_id = int(input("Enter member_id to update: ").strip())
            new_mail = (input("Enter new email: ").strip())
 
            updated = update_member(member_id, new_mail)
            if updated:
                print("Updated record:", updated)
            else:
                print("No record updated — check member_id.")

        elif ch==8:
            pid = int(input("Enter member_id to delete: ").strip())
            confirm = input(f"Are you sure you want to delete product {pid}? (yes/no): ").strip().lower()
            if confirm == "yes":
                deleted = delete_member(pid)
                if deleted:
                    print("Deleted:", deleted)
                else:
                    print("No product deleted — check member_id.")
            else:
                print("Delete cancelled.")

        elif ch==9:
            pid = int(input("Enter book_id to delete: ").strip())
            confirm = input(f"Are you sure you want to delete product {pid}? (yes/no): ").strip().lower()
            if confirm == "yes":
                deleted = delete_book(pid)
                if deleted:
                    print("Deleted:", deleted)
                else:
                    print("No product deleted — check book_id.")
            else:
                print("Delete cancelled.")
        elif ch==10:
            break
 
 