from typing import TYPE_CHECKING, Optional

from django.template.defaultfilters import slugify

if TYPE_CHECKING:
    from django.db.models import Model as DjangoModel

    _Slug = str
    _SlugField = str


def _get_initial_slug_params(
    instance: "DjangoModel",
    desired_slug: Optional[str],
    slugify_field: Optional[str],
    slug_field: Optional[str],
) -> "tuple[_Slug, _SlugField]":
    if desired_slug is None:
        try:
            name: str = getattr(instance, slugify_field or "name")
        except AttributeError:
            raise TypeError("slugify_field is required")

        desired_slug = name

    if slug_field is None:
        try:
            getattr(instance, "slug")
        except AttributeError:
            raise TypeError("slug_field is required")

        slug_field = "slug"

    slug = slugify(desired_slug)
    return slug, slug_field


def create_slug(
    instance: "DjangoModel",
    desired_slug: Optional[str] = None,
    slugify_field: Optional[str] = None,
    slug_field: Optional[str] = None,
    max_runs: int = 50,
) -> str:
    """Generate slug for a Django model instance.

    The Django model instance is expected to have a a 'slug' field that can be
    checked for uniqueness. The function will try to use the `desired_slug` if
    supplied, otherwise the `slugify_field` is required. If the slug is not
    unique the function will see if the slug ends with a hyphen and a numeric
    value. If the slug does end with a hyphen and a numeric value then it will
    increment the number and check for uniqueness (it will repeat this process
    until the maximum number of runs has been reached). If the slug does not
    end with a hyphen and a numeric value, then it will append '-1' to the slug
    and continue incrementing until a unique value has been obtained (or
    possibly error out).

    Parameters
    ----------
    instance
        The Django model instance.
    desired_slug
        The desired slug by the user.
    slugify_field
        The field to slugify if no `desired_slug` was provided.
    slug_field
        The field to check if the generated slug is unique.
    max_runs
        The maximum number of runs to make before erroring out.

    Returns
    -------
    str
        The unique slug.

    Raises
    ------
    TypeError
        If no `desired_slug` has been supplied and the `slugify_field` is None
        and the 'sluggable' field is not called 'name', or `slug_field` is None
        and the slug field on the model is not called 'slug'.
    ValueError
        If the maximum number of runs have been reached.

    Examples
    --------
    All of the examples below assumes the following model exists and that the
    database is empty:

    class Article(models.Model):
        name = models.CharField(max_length=40)
        slug = models.SlugField(blank=True, null=True)

    Slugifying a model with a unique `desired_slug`.

    >>> article = Article.objects.create(name="Michael Scott Rocks")
    >>> create_slug(
    ...    article,
    ...    desired_slug="Michael Scott Rocks",
    ...    slug_field="slug",
    ... )
    'michael-scott-rocks'

    Slugifying a model with a non-unique `desired_slug`.

    >>> article1 = Article.objects.create(name="Michael Scott Rocks")
    >>> article1.slug = create_slug(
    ...     article1,
    ...     desired_slug="Michael Scott Rocks",
    ...     slug_field="slug",
    ... )
    >>> article1.save()
    >>> article2 = Article.objects.create(name="Michael Scott Rocks")
    >>> create_slug(
    ...     article1,
    ...     desired_slug="Michael Scott Rocks",
    ...     slug_field="slug",
    ... )
    'michael-scott-rocks-1'

    Slugifying a model without a `desired_slug` and the slugified field is
    unique.

    >>> article = Article.objects.create(name="Michael Scott Rocks")
    >>> create_slug(article, slugify_field="name", slug_field="slug")
    'michael-scott-rocks'

    Slugifying a model without a `desired_slug` and the slugified field is
    not unique.

    >>> article1 = Article.objects.create(name="Michael Scott Rocks")
    >>> article1.slug = create_slug(
    ...    article1,
    ...    slugify_field="name",
    ...    slug_field="slug",
    ... )
    >>> article1.save()
    >>> article2 = Article.objects.create(name="Michael Scott Rocks")
    >>> create_slug(article2, slugify_field="name", slug_field="slug")
    'michael-scott-rocks-1'
    """
    slug, slug_field = _get_initial_slug_params(
        instance=instance,
        desired_slug=desired_slug,
        slugify_field=slugify_field,
        slug_field=slug_field,
    )
    Model = instance.__class__
    run = 0

    while Model.objects.filter(**{slug_field: slug}).exists() and run < max_runs:
        parts = slug.rsplit("-", maxsplit=1)
        if len(parts) == 2 and parts[1].isdigit():
            slugified, num = parts
            slug = f"{slugified}-{int(num) + 1}"
        else:
            slug += "-1"

        run += 1

    if run >= max_runs:
        raise ValueError(
            f"could not slugify {instance}, try increasing the max runs or "
            "passing in a unique desired slug"
        )

    return slug
