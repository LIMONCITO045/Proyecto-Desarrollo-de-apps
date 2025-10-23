from modelo.productodao import ProductoDAO

def main():
    productodao = ProductoDAO()
    
    print("\n=== Listando productos ===")
    productodao.listarProductos()
    
if __name__ == "__main__":
    main()