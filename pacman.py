import json
import random
import networkx as nx
import test_solution
import datetime

def solve(dataset_txt):
    dataset = json.loads(dataset_txt)
    base_id = 0

    G = nx.DiGraph()
    for edge in dataset['roads']:
        if edge['isOneWay']:
            G.add_edge(edge['intersectionId1'], edge['intersectionId2'], length=edge['length'], one_way=True)
        else:
            G.add_edge(edge['intersectionId1'], edge['intersectionId2'], length=edge['length'], one_way=False)
            G.add_edge(edge['intersectionId2'], edge['intersectionId1'], length=edge['length'], one_way=False)


    dist_to_base = nx.shortest_path_length(G, source=None, target=base_id, weight='length')    

    visited_roads = set()  
    curr_node = base_id  
    path = [base_id]  
    score = 0  

    for day_i in range(dataset['numDays']):
        battery_remaining = dataset['batteryCapacity']  

        while True:
            neighbors = list(G.neighbors(curr_node))
            random.shuffle(neighbors)
            
            # L'agorithme du choix du prochain noeud est là !
            # Commencez par trouver un meilleur algorithme que celui-ci
            # -------------------------------------------  
            best_next_node = None
            best_score = -1

            for nxt in neighbors:
                edge_len = G[curr_node][nxt]['length']
                if battery_remaining >= edge_len + dist_to_base[nxt]:
                    edge_score = edge_len if (curr_node, nxt) not in visited_roads else 0
                    if (curr_node, nxt) not in visited_roads:
                        edge_score *= 2  
                    if edge_score > best_score:
                        best_score = edge_score
                        best_next_node = nxt

            if best_next_node is None:
                next_node = base_id
            else:
                next_node = best_next_node
            
            # -------------------------------------------


            # Mise à jour du score si la route n'a pas été visitée
            if (curr_node, next_node) not in visited_roads:
                score += G[curr_node][next_node]['length']

            # Ajout des routes visitées dans les deux sens
            visited_roads.add((curr_node, next_node))
            visited_roads.add((next_node, curr_node))

            # Mise à jour de la batterie restante
            battery_remaining -= G[curr_node][next_node]['length']

            # Ajout du prochain noeud au chemin
            path.append(next_node)
            curr_node = next_node

            # On termine la journée si on est de retour à la base
            if curr_node == base_id:
                break

        print(f'End day {day_i+1} with {battery_remaining} battery')  # Message de fin de jour


    # Message de fin de routage
    print(f'Visited {len(visited_roads) // 2} / {len(dataset["roads"])} roads')
    print(f'Expected score: {score:_}')

    # Retour du résultat sous forme de chaîne JSON
    return json.dumps({"chargeStationId": base_id, "itinerary": path})



dataset_file = "7_london"
dataset = open(f'.\\datasets\\{dataset_file}.json').read()

print('---------------------------------')
print(f'Solving {dataset_file}')
solution = solve(dataset)
print('---------------------------------')
score, is_valid, message = test_solution.getSolutionScore(solution, dataset)

if is_valid:
    print('✅ Solution is valid!')
    print(f'Message: {message}')
    print(f'Score: {score:_}')
    
    save = input('Save solution? (y/n): ')
    if save.lower() == 'y':
        date = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        file_name = f'{dataset_file}_{score}_{date}'
        
        with open(f'.\\solutions\\{file_name}.json', 'w') as f:
            f.write(solution)
        print('Solution saved')
    else:
        print('Solution not saved')
    
else:
    print('❌ Solution is invalid')
    print(f'Message: {message}')


