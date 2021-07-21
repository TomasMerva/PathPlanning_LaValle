#!/usr/bin/python3
import time
from discrete_world import *


def draw_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()
        time.sleep(0.02)  # time delay for simulation
    current.make_start()


def l1_norm(pose1, pose2):
    x1, y1 = pose1
    x2, y2 = pose2
    return abs(x2-x1) + abs(y2-y1)


def AStarAlgorithm(draw, start, goal):
    open_set, came_from = {}, {}
    visited = [start]
    start.cost = 0
    # Initialize Qfunction with the start state
    open_set[start] = start.cost + l1_norm(start.get_index_pos(), goal.get_index_pos())

    while len(open_set) > 0:                                                    # line 2
        # Check if the pygame close button was pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 0

        # Q.GetFirst() (get state with the lowest cost-to-go)
        # and remove it from the list
        current_state = min(open_set.items(), key=lambda item: item[1] + l1_norm(item[0].get_index_pos(), goal.get_index_pos()))[0]      # line 3
        del open_set[current_state]

        # Current state will become dead state so its cost_to_come can become optimal
        optimal_cost_to_come = current_state.cost

        if current_state == goal:                                               # line 4
            print("Goal is reached")
            draw_path(came_from, current_state, draw)
            return 0

        for neighbor in current_state.neighbors:                                # line 6 and line 7
            if not neighbor.is_dead():
                # Compute cost-to-come + cost-to-go
                cost_to_come = (optimal_cost_to_come + neighbor.cost)

                if neighbor not in visited:                                     # line 8
                    neighbor.cost = cost_to_come

                    # add/change neighbor.cost into Q function
                    visited.append(neighbor)                                    # line 9
                    open_set[neighbor] = neighbor.cost                          # line 10

                    # For showing final path
                    came_from[neighbor] = current_state
                    # Visualize
                    if neighbor != start and neighbor != goal:
                        neighbor.make_alive()

                else:                                                           # line 11
                    if cost_to_come < neighbor.cost:                            # line 12
                        open_set[neighbor] = cost_to_come
                        # For showing final path
                        came_from[neighbor] = current_state

        # Make current state dead
        if current_state != start:
            current_state.make_dead()

        draw()
        time.sleep(0.01)  # time delay for simulation

    print("No solution can be found!")
    return -1


def main(width, rows, obstacles_flag):
    world = DiscreteWorld(width, rows)
    world.make_grid(obstacles_flag)

    # Start and goal position
    start_node, goal_node = None, None

    run = True
    while run:
        world.draw()
        # Check events
        for event in pygame.event.get():
            # Check if the close button was clicked
            if event.type == pygame.QUIT:
                run = False
            # Check if the left mouse button was pressed (selecting start,goal and obstacles)
            if pygame.mouse.get_pressed()[0]:
                # Create start_node
                if not start_node:
                    start_node = world.get_mouse_clicked_node()
                    start_node.make_start()
                # Create goal_node
                elif not goal_node:
                    goal_node = world.get_mouse_clicked_node()
                    if goal_node != start_node:
                        goal_node.make_goal()
                    else:
                        goal_node = None
                # Create obstacle_nodes
                else:
                    obstacle_node = world.get_mouse_clicked_node()
                    if obstacle_node != start_node and obstacle_node != goal_node:
                        obstacle_node.make_obstacle()

            # Check if the right mouse button was pressed (remove obstacles)
            elif pygame.mouse.get_pressed()[2]:
                node = world.get_mouse_clicked_node()
                if node.is_obstacle():
                    node.reset()

            if event.type == pygame.KEYDOWN:
                # start algorithm
                if event.key == pygame.K_SPACE and start_node and goal_node:
                    world.update_neighbors()
                    AStarAlgorithm(lambda: world.draw(), start_node, goal_node)
                # reset environment
                if event.key == pygame.K_DELETE:
                    start_node, goal_node = None, None
                    world.make_grid(obstacles_flag)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--rows', type=int, default=20)
    parser.add_argument('--width', type=int, default=800)
    parser.add_argument('--obstacles', type=bool, default=True)
    args = parser.parse_args()

    main(width=args.width, rows=args.rows, obstacles_flag=args.obstacles)
