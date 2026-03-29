FOLDER = "../../../data/integrated/"

FILES_CONFIG = [
    {
        'filename': 'integrated_CH3CHO_226551.624.fits',
        'name': ('CH3CHO', '-'),
        'latex_name': ('CH$_3$CHO $\\quad 12_{0,12} - 11_{0,11} \\quad E $', 226551.624)
    },
    {
        'filename': 'integrated_CH3OCHO_238157.342.fits', 
        'name': ('CH3OCHO', '-'),
        'latex_name': ('CH$_3$OCHO $\\quad 22_{0,22}-21_{0,21} \\quad A$', 238157.342)
    },
    {
        'filename': 'integrated_t-CH3CH2OH_234758.793.fits',
        'name': ('t-CH3CH2OH', '-'),
        'latex_name': ('t-CH$_3$CH$_2$OH $\\quad 6(3,4)-5(2,3)$', 234758.793)
    },
    {
        'filename': 'integrated_CH3CH2CN_225236.12.fits',
        'name': ('CH3CH2CN', '-'),
        'latex_name': ('CH$_3$CH$_2$CN $\\quad 25_{4,21}-24_{4,20} $', 225236.12)
    },
    {
        'filename': 'integrated_CH3OH_241767.234.fits',
        'name': ('CH3OH', '-'),
        'latex_name': ('CH$_3$OH $\\quad 5_{-1,5}-4_{-1,4} \\quad E $', 241767.234)
    },
    {
        'filename': 'integrated_CH3OH_241887.674.fits',
        'name': ('CH3OH', '-'),
        'latex_name': ('CH$_3$OH $\\quad 5_{2,3}-4_{2,2} A^{++} $', 241887.674)
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
    'sources': False,
    'levels_': True
}
