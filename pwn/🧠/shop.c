#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

// Product structure
struct Product {
    int id;
    char name[50];
    float price;
    int stock;
};

// Global inventory array
struct Product inventory[10];
int product_count = 0;

// Function prototypes
void display_menu();
void add_product();
void view_products();
void update_stock();
void search_product();
void perform_inventory_check(); // Our dummy function that will contain the gadget

// Dummy function that contains our pop rdi; ret gadget
// This function is never called during normal execution
void perform_inventory_check() {
    // This is a dummy inventory validation function
    // that happens to contain our ROP gadget
    printf("Performing inventory consistency check...\n");
    
    // This inline assembly code will generate our pop rdi; ret gadget
    __asm__(
        ".byte 0x5f, 0xc3"  // pop rdi; ret
    );
    
    // This code is never reached but makes the function look legitimate
    printf("Inventory check completed successfully.\n");
}

int main() {
    int choice;
    char username[30];
    
    // Initial welcome
    printf("TechnoShop Inventory Management System v1.0\n");
    printf("===========================================\n\n");
    
    // Get username - no vulnerability here, just for atmosphere
    printf("Please enter your username: ");
    fgets(username, sizeof(username), stdin);
    username[strcspn(username, "\n")] = 0; // Remove newline
    
    printf("\nWelcome, ");
    printf(username);
    
    // Main program loop
    while (1) {
        display_menu();
        printf("Enter your choice (1-5): ");
        scanf("%d", &choice);
        getchar(); // Consume newline
        
        switch (choice) {
            case 1:
                add_product();
                break;
            case 2:
                view_products();
                break;
            case 3:
                update_stock();
                break;
            case 4:
                search_product();
                break;
            case 5:
                printf("Thank you for using TechnoShop Inventory System.\n");
                return 0;
            default:
                printf("Invalid choice! Please try again.\n");
        }
        
        printf("\nPress Enter to continue...");
        getchar();
    }
    
    return 0;
}

void display_menu() {
    printf("\n\n==== MAIN MENU ====\n");
    printf("1. Add New Product\n");
    printf("2. View All Products\n");
    printf("3. Update Stock\n");
    printf("4. Search Product\n");
    printf("5. Exit\n");
}

void add_product() {
    if (product_count >= 10) {
        printf("Inventory is full! Cannot add more products.\n");
        return;
    }
    
    struct Product new_product;
    printf("\n==== ADD NEW PRODUCT ====\n");
    
    new_product.id = product_count + 1001;
    
    printf("Enter product name: ");
    char buffer[50];
    fgets(buffer, sizeof(buffer), stdin);
    buffer[strcspn(buffer, "\n")] = 0;
    strcpy(new_product.name, buffer);
    
    printf("Enter price: $");
    scanf("%f", &new_product.price);
    
    printf("Enter initial stock: ");
    scanf("%d", &new_product.stock);
    getchar(); // Consume newline
    
    inventory[product_count++] = new_product;
    printf("\nProduct added successfully! ID: %d\n", new_product.id);
}

void view_products() {
    printf("\n==== PRODUCT INVENTORY ====\n");
    if (product_count == 0) {
        printf("No products in inventory.\n");
        return;
    }
    
    printf("ID\tName\t\t\tPrice\tStock\n");
    printf("------------------------------------------------\n");
    
    for (int i = 0; i < product_count; i++) {
        printf("%d\t%-20s\t$%.2f\t%d\n", 
               inventory[i].id, 
               inventory[i].name, 
               inventory[i].price, 
               inventory[i].stock);
    }
}

void update_stock() {
    int id, new_stock;
    int found = 0;
    
    printf("\n==== UPDATE STOCK ====\n");
    printf("Enter product ID: ");
    scanf("%d", &id);
    getchar(); // Consume newline
    
    for (int i = 0; i < product_count; i++) {
        if (inventory[i].id == id) {
            printf("Current stock for '%s': %d\n", inventory[i].name, inventory[i].stock);
            printf("Enter new stock amount: ");
            scanf("%d", &new_stock);
            getchar(); // Consume newline
            
            inventory[i].stock = new_stock;
            printf("Stock updated successfully!\n");
            found = 1;
            break;
        }
    }
    
    if (!found) {
        printf("Product with ID %d not found!\n", id);
    }
}

void search_product() {
    char search_term[100]; // Vulnerable buffer
    char temp[50];
    int found = 0;
    
    printf("\n==== SEARCH PRODUCT ====\n");
    printf("Enter search term: ");
    // Vulnerable function - can read more than buffer size
    fgets(search_term, 0x100, stdin); // 0x100 = 256 bytes
    search_term[strcspn(search_term, "\n")] = 0; // Remove newline
    
    printf("\nSearch results for '%s':\n", search_term);
    printf("------------------------------------------------\n");
    
    for (int i = 0; i < product_count; i++) {
        strcpy(temp, inventory[i].name);
        if (strstr(temp, search_term) != NULL) {
            printf("ID: %d, Name: %s, Price: $%.2f, Stock: %d\n", 
                   inventory[i].id, 
                   inventory[i].name, 
                   inventory[i].price, 
                   inventory[i].stock);
            found = 1;
        }
    }
    
    if (!found) {
        printf("No products found matching '%s'.\n", search_term);
    }
}
