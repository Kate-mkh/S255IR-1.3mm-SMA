FOLDER = "../../data/integrated/"

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
        'filename': 'integrated_CH3OH_241887.674.fits',
        'name': ('CH3OH', '-'),
        'latex_name': ('CH$_3$OH $\\quad 5_{2}-4_{2} \\quad A^{+} $', 241887.674),
        'beam': True,
        'markers': True,
        'sources': False,
        'levels_': True
    },      
    {
        'filename': 'integrated_CH3OH_218440.05.fits',
        'name': ('CH3OH', '-'),
        'latex_name': ('CH$_3$OH $\\quad 4₂-3₁ \\quad E $', 218440.05),
        'beam': True,
        'markers': True,
        'sources': True,
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
    },
    {
        'name': 'met1',
        'ra_hms': [6, 12, 53.64946],
        'dec_dms': [17, 59, 26.2884],
        'marker': 'x',  
        'color': 'white',
        'size': 60,
        'label_x_pix': 85,
        'label_y_pix': 75,
        'line': True,
        'line_start_x': 85,  
        'line_start_y': 75,
        'line_end_x': 66,    
        'line_end_y': 68.5,
        'line_color': 'black',
        'line_width': 1,
        'line_style': '-'        
    },
    {
        'name': 'met2',
        'ra_hms': [6, 12, 53.22395],
        'dec_dms': [17, 59, 24.2448],
        'marker': 'x',  
        'color': 'white',
        'size': 60,
        'label_x_pix': 90,
        'label_y_pix': 70,
        'line': True,
        'line_start_x': 90,  
        'line_start_y': 70,
        'line_end_x': 78,    
        'line_end_y': 64,
        'line_color': 'black',
        'line_width': 1,
        'line_style': '-'        
    }
]