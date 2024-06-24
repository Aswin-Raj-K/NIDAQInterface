import nptdms as td

with td.TdmsFile.open('DEMO_file.tdms') as file:
    for prop in file.properties:
        print(f'{prop}: {file.properties[prop]}', end=' | ')
    print('')

    for group in file.groups():
        print(':::::')
        print(group.name, end=' | ')
        for prop in group.properties:
            print(f'{prop}: {group.properties[prop]}', end=' | ')
        print('')
        for channel in group.channels():
            print(f'  {channel.name}')
            print(f'    {channel[:]}')
