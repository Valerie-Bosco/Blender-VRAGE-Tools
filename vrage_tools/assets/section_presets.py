'''
Section Preset Menu is split into columns 
and categories according to this structure:

[   column{     category:(item, item), 
                category:(item, item) },
    column{     category:(item, item), 
                category:(item, item) }, ...]
                
'''
section_presets  = [
    {
        "Conveyor":(
            "ConveyorFront",
            "ConveyorBack",
            "ConveyorLeft",
            "ConveyorRight",
            "ConveyorTop",
            "ConveyorBottom",
        ),
        "Terminal":(
            "TerminalFront",
            "TerminalBack",
            "TerminalLeft",
            "TerminalRight",
            "TerminalTop",
            "TerminalBottom",
        ),
    },
    {
        "Button":(
            "ButtonFront",
            "ButtonBack",
            "ButtonLeft",
            "ButtonRight",
            "ButtonTop",
            "ButtonBottom",
        ),
        "Misc":(
            "PowerUsageSlot_Front",
            "ProductionSpeedSlot_Front",
            "PowerCellHousing_01",
        ),
    }
]