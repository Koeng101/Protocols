from opentrons import labware, instruments, robot, modules
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'PCR Prep 4/4: PCR',
    'author': 'Chaz <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

tempdeck = modules.load('tempdeck', '4')
tempplate = labware.load('biorad_96_wellplate_200ul_pcr', '4', share=True)
tempdeck.set_temperature(4)
tempdeck.wait_for_temp()
pcr_well = labware.load('opentrons_96_aluminumblock_generic_pcr_strip_200ul',
                        '5', 'chilled aluminum block w/ PCR strip')
primer_plate = labware.load(
            'biorad_96_wellplate_200ul_pcr', '1', 'primer plate')
dna_plate = labware.load(
            'biorad_96_wellplate_200ul_pcr', '6', 'DNA plate')
tipracks = [
    labware.load('tiprack-10ul', slot) for slot in ['7', '8', '9']
]


def run_custom_protocol(
        p10_mount: StringSelection('left', 'right') = 'left',
):

    # create pipette

    pip10 = instruments.P10_Multi(mount=p10_mount, tip_racks=tipracks)

    tip10_max = len(tipracks)*12
    tip10_count = 0

    def pick_up(pip):
        nonlocal tip10_count

        if tip10_count == tip10_max:
            robot.pause(
                'Replace 10ul tipracks in slots 7, 8, and 9 before resuming.')
            pip10.reset()
            tip10_count = 0
        pip10.pick_up_tip()
        tip10_count += 1

    dest = tempplate.rows('A')[:12]
    primers = primer_plate.rows('A')[:12]
    samps = dna_plate.rows('A')[:12]

    # step 1

    pick_up(pip10)

    for d in dest:
        pip10.transfer(8.7, pcr_well.wells('A1'), d, new_tip='never')
        pip10.blow_out(d.top())

    pip10.drop_tip()

    # step 2

    for p, d in zip(primers, dest):
        pick_up(pip10)
        pip10.transfer(1.3, p, d, new_tip='never')
        pip10.blow_out(d.top())
        pip10.drop_tip()

    # step 3

    for s, d in zip(samps, dest):
        pick_up(pip10)
        pip10.transfer(5, s, d, new_tip='never')
        pip10.blow_out(d.top())
        pip10.drop_tip()

    robot.comment("Congratulations, you have completed step 4/4 of this \
    protocol. Please remove samples from OT-2 and properly store.")