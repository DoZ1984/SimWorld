from world.world import World, WorldConfig

def main():
    """Main simulation loop"""
    print("Simulación iniciada...\n")
    
    config = WorldConfig(
        initial_population=1000,
        region_count=5,
        initial_resources={
            "food": 10000.0,
            "water": 20000.0,
            "energy": 15000.0,
            "minerals": 5000.0
        }
    )
    
    world = World(config)
    
    # Simulate for 10 years
    for _ in range(10):
        stats = world.get_statistics()
        current_year = stats["year"]
        
        print(f"Año {current_year}:")
        print(f"Población: {stats['population']}")
        print(f"Corporaciones: {stats['corporations']}")
        print(f"Precios de mercado: {stats['market_prices']}")
        print(f"Estado político: {stats['political_state']}")
        print(f"Riqueza promedio: ${stats['average_wealth']:.2f}")
        print()
        
        if not world.update():
            break
    
    print("Simulación finalizada")

if __name__ == "__main__":
    main() 