from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Restaurant(models.Model):

    name = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=200)
    image_url = models.URLField("Image URL", max_length=350, null=True, blank=True)
    latitude = models.DecimalField(
        max_digits=8, decimal_places=5, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=8, decimal_places=5, null=True, blank=True
    )
    rating = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ("name", "-rating")
        constraints = [
            models.CheckConstraint(
                check=models.Q(rating__lte=5), name="restaurant_rating_lte_5"
            ),
        ]

    def get_absolute_url(self):
        return reverse("recommender:restaurant-detail", args=[str(self.id)])

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # latitude and longitude have values only when both are given
        if not (self.longitude and self.latitude):
            self.longitude = None
            self.latitude = None
        # Create slug from name
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Dish(models.Model):

    restaurant = models.ForeignKey(
        Restaurant, related_name="dishes", on_delete=models.CASCADE
    )
    name = models.CharField("Dish name", max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    rating = models.PositiveIntegerField(null=True, blank=True)
    image_url = models.URLField("Image URL", max_length=350, null=True, blank=True)

    class Meta:
        ordering = ("name", "-price", "-rating")
        verbose_name_plural = "Dishes"
        constraints = [
            models.CheckConstraint(
                check=models.Q(rating__lte=5), name="dish_rating_lte_5"
            )
        ]

    def get_absolute_url(self):
        return reverse(
            "recommender:dish-detail",
            kwargs={"restaurant_id": str(self.restaurant.id), "dish_id": str(self.id)},
        )

    def __str__(self):
        return self.name
