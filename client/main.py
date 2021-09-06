from base_window import Base_window
import server_interface

parameters = {
    'MILLISEC_PER_FRAME': 50,
    'mascot_path': 'mascot.gif',
    'background_path': 'background.jpg',
    'window_width': 1000,
    'window_height': 500,
    'window_title': 'Study Buddy'
}
parameters['aspect_ratio'] = (parameters['window_width'] /
                              parameters['window_height'])

base = Base_window(parameters)
