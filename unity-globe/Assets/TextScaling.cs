using UnityEngine;
using TMPro;

public class TextScaling : MonoBehaviour
{
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    public TMP_Text[] texts;
    [SerializeField] private GameObject LocaleText;
    [SerializeField] private float scaleFactor;
    [SerializeField] private CameraRotation cameraRotation;
    void Start()
    {
        texts = LocaleText.GetComponentsInChildren<TMP_Text>(true);
    }

    // Update is called once per frame
    void Update()
    {
        foreach (TMP_Text text in texts)
        {
            text.fontSize = Mathf.Abs((cameraRotation.Limits.y)/(cameraRotation.Limits.x) * cameraRotation.PositionZoom * scaleFactor);
        }
    }
}
