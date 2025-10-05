using UnityEngine;
using UnityEngine.InputSystem;

public class CameraRotation : MonoBehaviour
{
    [SerializeField] private InputAction Look;
    [SerializeField] private InputAction Zoom;
    [SerializeField] private InputControl control;
    [SerializeField] private InputActionAsset inputActions;
    private Vector3 AddingInput;
    private Vector3 PositonInput;
    private Vector3 velocity = Vector3.zero;

    private float AddingZoom;
    public float PositionZoom;
    private float zoomVelocity = 0;
    [SerializeField] private Vector2 sens;
    [SerializeField] private float zoomSens;
    [SerializeField] private Transform EarthZoom;
    [SerializeField] public Vector2 Limits;
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        Look = inputActions.FindAction("Look");
        Zoom = inputActions.FindAction("Zoom");
        Look.Enable();
    }

    // Update is called once per frame
    void Update()
    {

        AddingInput.y -= Look.ReadValue<Vector2>().x * sens.x * Mathf.Abs((Limits.y / Limits.x) * PositionZoom);
        AddingInput.x += Look.ReadValue<Vector2>().y * sens.y * Mathf.Abs((Limits.y / Limits.x) * PositionZoom);
        PositonInput.x += AddingInput.x * Time.deltaTime;
        PositonInput.y += AddingInput.y * Time.deltaTime;

        AddingZoom += Zoom.ReadValue<float>() * zoomSens;
        PositionZoom += AddingZoom * Time.deltaTime;

        AddingInput = Vector3.SmoothDamp(AddingInput, Vector3.zero, ref velocity, 0.1f);
        AddingZoom = Mathf.SmoothDamp(AddingZoom, 0, ref zoomVelocity, 0.1f);
        PositionZoom = Mathf.Clamp(PositionZoom, Limits.x, Limits.y);

        transform.localEulerAngles = PositonInput;
        EarthZoom.localPosition = new Vector3(0, 0, PositionZoom);
    }
}
