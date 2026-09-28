from client import ConnectedComponentsLabeler

def main():
    ccl = ConnectedComponentsLabeler(connectivity=8)
    blob_map = [[0]*10 for _ in range(10)]
    blob_map[1][1] = blob_map[1][2] = blob_map[2][1] = 1
    blob_map[6][6] = blob_map[6][7] = blob_map[7][7] = 1
    res = ccl.label_components(blob_map)
    print("Connected Components Labeler Verification:")
    print(f"Total Components: {res['num_components']}")
    for c in res['components']:
        print(f"  Component {c['label']}: Area={c['area']}, BoundingBox=({c['min_x']},{c['min_y']})-({c['max_x']},{c['max_y']})")

if __name__ == "__main__":
    main()
