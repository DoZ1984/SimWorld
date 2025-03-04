from world.world import World, WorldConfig

def main():
    config = WorldConfig(
        population_size=10000,
        start_year=2024,
        initial_resources={
            'oil': 1e6,
            'food': 5e5,
            'water': 2e9
        }
    )
    
    world = World(config)
    print("Simulación iniciada...")
    
    try:
        while True:
            world.run(years=1)
            # Actualizar interfaz y estadísticas
    except KeyboardInterrupt:
        print("Simulación detenida")

if __name__ == "__main__":
    main() 