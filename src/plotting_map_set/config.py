FOLDER = "../../outputs/integrated/"

LANGUAGE_SETTINGS = {
    'language': 'en',  # 'en' or 'ru'
    'frequency_unit': 'MHz',  # 'MHz' or 'МГц'
}

VISUAL_SETTINGS = {
    'cmap': 'YlOrRd', 
    'contours_percent': [0.25, 0.5, 0.75],
    'shift_x': 1.2,
    'shift_y': 1.2,
    'size_x': 4.5,
    'size_y': 4,
    'gap': 0.01       
}

FILES_CONFIG = [
    {
        'filename': 'integrated_CH3OH_218440.05.fits',
        'name': ('CH3OH', '-'),
        'latex_name': ('CH$_3$OH $transition \\quad $', 218440.05),
        'beam': True,
        'markers': True,
        'sources': False,
        'levels_': True
    },      
    {
        'filename': 'integrated_H2CO_218222.195.fits', 
        'name': ('H2CO', '-'),
        'latex_name': ('H$_2$CO $transition \\quad $', 218222.195),
        'beam': True,
        'markers': True,
        'sources': False,
        'levels_': True
    }
]

PLOT_SETTINGS = {
    'x_0': 30,
    'x_end': 100, 
    'y_0': 30,
    'y_end': 90,
    'cols': 2,
    'beam': True,
    'markers': True,
    'sources': True,
    'levels_': True
}

SOURCES_CONFIG = [
    {
        'name': '',
        'ra_deg': 93.225,  
        'dec_deg': 17.989755555555554,  
        'marker': '^',  
        'color': 'black',
        'size': 80,
        'label_x_pix': 50,  
        'label_y_pix': 56,
        'line': False,  
        'line_start_x': 45,  
        'line_start_y': 52,
        'line_end_x': 50,   
        'line_end_y': 56,
        'line_color': 'black',
        'line_width': 1,
        'line_style': '--'
    },
    {
        'name': '', 
        'ra_hms': [6, 12, 53.77500],
        'dec_dms': [17, 59, 26.17],
        'marker': '^',
        'color': 'black',
        'size': 80,
        'label_x_pix': 66,
        'label_y_pix': 70,
        'line': False  
    },
    {
        'name': '',
        'ra_hms': [6, 12, 53.84300],
        'dec_dms': [17, 59, 23.6200],
        'marker': '^',
        'color': 'black',
        'size': 80,
        'label_x_pix': 63,
        'label_y_pix': 58,
        'line': False
    }
]