using UnityEngine;

public class PlaceItemOnGlobe : MonoBehaviour
{
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    [SerializeField] private float DistanceFromCenter;
    [SerializeField] private Vector3 LatLongHeight; // X = Latitude, Y = Longitude, Z = Height from surface
    [SerializeField] private GameObject GlobeTemplateItem;
    [SerializeField] private GameObject GlobeItemPlace;
    [SerializeField] private int NumberOfItemsToPlace;
    [SerializeField] private float MinScale;
    void Start()
    {
        for (int i = 0; i < NumberOfItemsToPlace; i++)
        {
            PlaceItem();
        }
    }

    // Update is called once per frame
    void Update()
    {
    }
    void PlaceItem()
    {
        LatLongHeight.x = Random.Range(-90f, 90f); // Latitude
        LatLongHeight.y = Random.Range(-180f, 180f); // Longitude
        transform.eulerAngles = new Vector3(-LatLongHeight.x, LatLongHeight.y - 90, 0);
        GlobeTemplateItem.transform.position = transform.position + transform.forward * DistanceFromCenter;
        GlobeTemplateItem.transform.rotation = transform.rotation;
        GameObject Item = Instantiate(GlobeItemPlace, GlobeTemplateItem.transform.position, GlobeTemplateItem.transform.rotation);
        Item.transform.localScale = new Vector3(MinScale, MinScale, Random.Range(0.1f, 5));
    }
}
