from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from unixtimestampfield.fields import UnixTimeStampField


def validateValueIsAtLeast(value, threshold, valueName="Value"):
    if value < threshold:
        raise ValidationError(f"{valueName} must be at least {threshold}.")


class Food(models.Model):
    id = models.BigAutoField(primary_key=True)
    barcode = models.TextField(null=True, unique=True)
    name = models.TextField(null=True)
    kilojoulesPerGram = models.FloatField(validators=[MinValueValidator(0)])
    gramsOfProteinPerGram = models.FloatField(validators=[MinValueValidator(0)], default=0)
    gramsOfFatPerGram = models.FloatField(validators=[MinValueValidator(0)], default=0)
    gramsOfSaturatedFatPerGram = models.FloatField(validators=[MinValueValidator(0)], default=0)
    gramsOfCarbohydratePerGram = models.FloatField(validators=[MinValueValidator(0)], default=0)
    gramsOfSugarPerGram = models.FloatField(validators=[MinValueValidator(0)], default=0)
    gramsOfSodiumPerGram = models.FloatField(validators=[MinValueValidator(0)], default=0)

    def validate(self):
        # Validate above zero
        validateValueIsAtLeast(self.kilojoulesPerGram, 0, "kilojoulesPerGram")
        validateValueIsAtLeast(self.gramsOfProteinPerGram, 0, "gramsOfProteinPerGram")
        validateValueIsAtLeast(self.gramsOfFatPerGram, 0, "gramsOfFatPerGram")
        validateValueIsAtLeast(self.gramsOfSaturatedFatPerGram, 0, "gramsOfSaturatedFatPerGram")
        validateValueIsAtLeast(self.gramsOfCarbohydratePerGram, 0, "gramsOfCarbohydratePerGram")
        validateValueIsAtLeast(self.gramsOfSugarPerGram, 0, "gramsOfSugarPerGram")
        validateValueIsAtLeast(self.gramsOfSodiumPerGram, 0, "gramsOfSodiumPerGram")
        
        # Validate nutritional content
        sum = self.gramsOfProteinPerGram\
            + self.gramsOfFatPerGram\
            + self.gramsOfSaturatedFatPerGram\
            + self.gramsOfCarbohydratePerGram\
            + self.gramsOfSugarPerGram\
            + self.gramsOfSodiumPerGram

        if sum > 1:
            raise ValidationError("The sum of grams of nutritional content per gram can not be greater than one.")


    def isValid(self) -> bool:
        try:
            self.validate()
            return True
        except ValidationError:
            pass
        return False

    def save(self):
        self.validate()
        super().save()


class Consumption(models.Model):
    id = models.BigAutoField(primary_key=True)
    time = UnixTimeStampField(auto_now_add=True, use_numeric=True)
    foodId = models.ForeignKey(Food, on_delete=models.PROTECT)
    weightGrams = models.FloatField(validators=[MinValueValidator(0)])

    def validate(self):
        validateValueIsAtLeast(self.weightGrams, 0)

    def isValid(self) -> bool:
        try:
            self.validate()
            return True
        except ValidationError:
            pass
        return False

    def save(self):
        self.validate()
        super().save()


class Favorite(models.Model):
    id = models.IntegerField(primary_key=True, validators=[MaxValueValidator(9999), MinValueValidator(0)])
    foodId = models.OneToOneField(Food, on_delete=models.CASCADE)

    def validate(self):
        if self.id < 0 or 9999 < self.id:
            raise ValidationError("id must be between 0 and 9999 (must be four digits)")
        

    def isValid(self) -> bool:
        try:
            self.validate()
            return True
        except ValidationError:
            pass
        return False

    def save(self):
        self.validate()
        super().save()
