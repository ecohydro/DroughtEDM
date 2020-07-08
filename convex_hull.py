def con_hull_vol(indir):
    files = np.array(os.listdir(indir))
    csvs = pd.Series(files).str.contains('.csv')
    files = files[csvsvs]
    cols = ['NDVI', 'Precip', 'SM', 'LST', 'Temp', 'RefET']
    output = []
    
    for filename in files:
        for column in cols:
            for i in range(1,37):
                data = df.loc[i]
                pc = PyntCloud(data)
                con_hull_id = pc.add_structure('convex_hull')
                con_hull = pc.structures[con_hull_id]
                pc.mesh = con_hull.get_mesh()
                vol = con_hull.volume
                output.append(
                {
                    'dekad': i,
                    'volume': vol,
                }
            )
    
    return pd.DataFrame(output)


csvs = [file for file in sorted(os.listdir(indir)) if file[-4:] == '.csv']

