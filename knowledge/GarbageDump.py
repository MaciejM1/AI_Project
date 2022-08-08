from knowledge.Sector import *

# Klasa wysypiska śmieci
class GarbageDump:
    def __init__(self, image, startCol, startRow):
        # Numer kolumny startowej
        self.startCol = startCol
        # Numer wiersza startowego
        self.startRow = startRow
        # Ikona
        self.GarbageDumpImage = image
        # Sektor tworzyw sztucznych i metali
        self.plastic_and_metal_sector = Sector(SectorType.PLASTIC_AND_METAL, 1, 6, RECYCLE_YELLOW_RESIZED)
        # Sektor szkła
        self.glass_sector = Sector(SectorType.GLASS, 2, 6, RECYCLE_GREEN_RESIZED)
        # Sektor papieru
        self.paper_sector = Sector(SectorType.PAPER, 3, 6, RECYCLE_BLUE_RESIZED)
        # Sektor bioodpadów
        self.bio_sector = Sector(SectorType.BIO, 4, 6, BIN_BROWN_RESIZED)
